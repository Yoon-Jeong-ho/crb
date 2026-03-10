from __future__ import annotations

import json
import logging
import random
import signal
import traceback
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Iterable

from crb.config import load_run_config
from crb.datasets import load_items
from crb.datasets import hf_loaders  # noqa: F401  # register HF loaders
from crb.engines import create_engine
from crb.evaluation.scorers import normalize_gold_answer, score_output
from crb.io.results import append_jsonl, append_scoreboard, read_jsonl, write_json
from crb.prompts.templates import (
    build_flattened_prompt,
    build_multi_turn_messages,
    render_question_block,
    render_single_turn_prompt,
)
from crb.sampling.dummy_sampler import build_or_load_manifest, manifest_entry_lookup
from crb.schemas import HistoryTurn, NormalizedItem, RunConfig, dataclass_to_dict
from crb.utils.git import get_git_commit
from crb.utils.logging import configure_logging
from crb.utils.paths import config_hash, run_root
from crb.utils.runtime import compact_timestamp, utc_timestamp


class TimeoutException(RuntimeError):
    """Raised when an inference call exceeds the configured deadline."""


@contextmanager

def _timeout(seconds: int | None):
    if not seconds:
        yield
        return

    def _handler(signum, frame):  # type: ignore[no-untyped-def]
        raise TimeoutException(f"Timed out after {seconds} seconds")

    previous = signal.signal(signal.SIGALRM, _handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)



def run_from_config(config_path: str | Path) -> dict:
    config = load_run_config(config_path)
    return execute_run(config)



def execute_run(config: RunConfig) -> dict:
    signature = config_hash(config)
    run_dir = run_root(config)
    run_dir.mkdir(parents=True, exist_ok=True)
    final_jsons = sorted(run_dir.glob("run-*.json"))
    if final_jsons and config.runtime.skip_completed:
        return json.loads(final_jsons[-1].read_text(encoding="utf-8"))

    log_path = Path(config.runtime.log_dir) / f"{config.experiment.name}__{signature}.log"
    logger = configure_logging(log_path)
    logger.info("Loading datasets for experiment %s", config.experiment.name)

    target_items = _prepare_items(load_items(config.evaluation.target), config.evaluation.target, config.experiment.num_samples)
    dummy_items = _load_dummy_items(config)
    manifest, manifest_file, created = build_or_load_manifest(
        config=config,
        target_items=target_items,
        dummy_items=dummy_items,
    )
    logger.info("Using manifest %s (%s)", manifest_file, "created" if created else "reused")
    manifest_lookup = manifest_entry_lookup(manifest)
    dummy_index = {item.item_id: item for item in dummy_items}

    partial_path = run_dir / "partial_results.jsonl"
    partial_results = read_jsonl(partial_path) if config.runtime.resume else []
    completed_ids = {record["item_id"] for record in partial_results}
    ordered_results = {record["item_id"]: record for record in partial_results}

    engine = create_engine(config)
    try:
        for item in target_items:
            if item.item_id in completed_ids:
                logger.info("Skipping completed item %s", item.item_id)
                continue
            logger.info("Evaluating item %s", item.item_id)
            try:
                item_result = _evaluate_target_item(
                    item=item,
                    config=config,
                    dummy_index=dummy_index,
                    manifest_lookup=manifest_lookup,
                    engine=engine,
                )
            except Exception as exc:  # noqa: BLE001
                logger.error("Item %s failed: %s", item.item_id, exc)
                logger.error(traceback.format_exc())
                item_result = _build_runtime_failure(item, exc)
            ordered_results[item.item_id] = item_result
            append_jsonl(partial_path, item_result)
    finally:
        engine.close()

    per_item_results = [ordered_results[item.item_id] for item in target_items if item.item_id in ordered_results]
    metrics = _compute_metrics(per_item_results)
    run_id = f"run-{compact_timestamp()}-{signature[:8]}"
    payload = {
        "run_id": run_id,
        "timestamp": utc_timestamp(),
        "git_commit": get_git_commit(Path.cwd()),
        "model_name": config.model.model_name,
        "engine": config.model.engine,
        "dataset": config.evaluation.target.dataset_name,
        "split": config.evaluation.target.split,
        "evaluation_mode": config.evaluation.evaluation_mode,
        "history_mode": config.evaluation.history_mode,
        "dummy_type": config.evaluation.dummy_type,
        "k": config.evaluation.k,
        "seed": config.experiment.seed,
        "num_items": len(per_item_results),
        "metrics": metrics,
        "manifest_path": str(manifest_file),
        "config": config.to_dict(),
        "per_item_results": per_item_results,
    }
    output_path = run_dir / f"{run_id}.json"
    write_json(output_path, payload)
    append_scoreboard(
        config.runtime.summary_csv,
        {
            "timestamp": payload["timestamp"],
            "run_id": run_id,
            "git_commit": payload["git_commit"],
            "model_name": payload["model_name"],
            "dataset": payload["dataset"],
            "split": payload["split"],
            "evaluation_mode": payload["evaluation_mode"],
            "history_mode": payload["history_mode"],
            "dummy_type": payload["dummy_type"],
            "k": payload["k"],
            "seed": payload["seed"],
            "num_items": payload["num_items"],
            "accuracy": metrics["accuracy"],
            "format_failure_rate": metrics["format_failure_rate"],
            "result_json_path": str(output_path),
        },
    )
    logger.info("Completed run %s with accuracy %.4f", run_id, metrics["accuracy"])
    return payload



def _prepare_items(
    items: list[NormalizedItem],
    source_config,
    limit_override: int | None,
) -> list[NormalizedItem]:
    working = list(items)
    if source_config.shuffle:
        rng = random.Random(source_config.seed)
        rng.shuffle(working)
    if source_config.limit is not None:
        working = working[: source_config.limit]
    if limit_override is not None:
        working = working[:limit_override]
    return working



def _load_dummy_items(config: RunConfig) -> list[NormalizedItem]:
    combined: list[NormalizedItem] = []
    sources = config.evaluation.dummy_sources or [config.evaluation.target]
    for source in sources:
        combined.extend(_prepare_items(load_items(source), source, source.limit))
    return combined



def _evaluate_target_item(
    *,
    item: NormalizedItem,
    config: RunConfig,
    dummy_index: dict[str, NormalizedItem],
    manifest_lookup: dict[str, object],
    engine,
) -> dict:
    manifest_entry = manifest_lookup[item.item_id]
    dummy_ids = manifest_entry.dummy_ids_by_type[config.evaluation.dummy_type][: config.evaluation.k]
    history_turns: list[HistoryTurn] = []
    if config.evaluation.history_mode == "oracle_history":
        for dummy_id in dummy_ids:
            dummy_item = dummy_index[dummy_id]
            history_turns.append(
                HistoryTurn(
                    item_id=dummy_item.item_id,
                    question=render_question_block(dummy_item),
                    choices=dummy_item.choices,
                    normalized_answer=normalize_gold_answer(dummy_item),
                    raw_output=None,
                    answer_source="oracle",
                    parse_status="oracle",
                    dataset_name=dummy_item.dataset_name,
                    subject=dummy_item.subject,
                    domain=dummy_item.domain,
                )
            )
    else:
        for dummy_id in dummy_ids:
            dummy_item = dummy_index[dummy_id]
            dummy_prompt = _render_prompt_for_generation(
                item=dummy_item,
                history=history_turns,
                config=config,
                engine=engine,
                force_multi_turn=True,
            )
            raw_dummy_output = _generate_with_timeout(engine.generate, dummy_prompt, config.runtime.timeout_seconds)
            dummy_score = score_output(dummy_item, raw_dummy_output)
            history_turns.append(
                HistoryTurn(
                    item_id=dummy_item.item_id,
                    question=render_question_block(dummy_item),
                    choices=dummy_item.choices,
                    normalized_answer=dummy_score.parsed.normalized_answer,
                    raw_output=raw_dummy_output,
                    answer_source="self",
                    parse_status=dummy_score.parsed.status,
                    error_type=dummy_score.parsed.error_type,
                    dataset_name=dummy_item.dataset_name,
                    subject=dummy_item.subject,
                    domain=dummy_item.domain,
                )
            )

    final_prompt = _render_prompt_for_generation(
        item=item,
        history=history_turns,
        config=config,
        engine=engine,
        force_multi_turn=False,
    )
    raw_output = _generate_with_timeout(engine.generate, final_prompt, config.runtime.timeout_seconds)
    score = score_output(item, raw_output)
    return {
        "item_id": item.item_id,
        "dataset_name": item.dataset_name,
        "split": item.split,
        "domain": item.domain,
        "subject": item.subject,
        "question": item.question,
        "choices": item.choices,
        "dummy_ids": dummy_ids,
        "dummy_turns": [dataclass_to_dict(turn) for turn in history_turns],
        "raw_output": raw_output,
        "parsed_answer": score.parsed.normalized_answer,
        "gold_answer": score.gold_answer,
        "normalized_gold_answer": score.normalized_gold_answer,
        "correct": score.is_correct,
        "parse_status": score.parsed.status,
        "parser_name": score.parsed.parser_name,
        "error_type": score.parsed.error_type,
        "prompt_preview": final_prompt[-1200:],
    }



def _render_prompt_for_generation(
    *,
    item: NormalizedItem,
    history: list[HistoryTurn],
    config: RunConfig,
    engine,
    force_multi_turn: bool,
) -> str:
    use_multi_turn = force_multi_turn or config.evaluation.evaluation_mode == "multi_turn"
    if use_multi_turn:
        messages = build_multi_turn_messages(
            history=history,
            target_item=item,
            prompt_config=config.prompt,
        )
        if hasattr(engine, "render_chat"):
            return engine.render_chat(messages)
        return "\n\n".join(f"{m['role'].upper()}: {m['content']}" for m in messages)
    return build_flattened_prompt(history=history, target_item=item, prompt_config=config.prompt)



def _generate_with_timeout(
    generate_fn: Callable[[str], str],
    prompt: str,
    timeout_seconds: int | None,
) -> str:
    with _timeout(timeout_seconds):
        return generate_fn(prompt)



def _build_runtime_failure(item: NormalizedItem, exc: Exception) -> dict:
    return {
        "item_id": item.item_id,
        "dataset_name": item.dataset_name,
        "split": item.split,
        "domain": item.domain,
        "subject": item.subject,
        "question": item.question,
        "choices": item.choices,
        "dummy_ids": [],
        "dummy_turns": [],
        "raw_output": "",
        "parsed_answer": None,
        "gold_answer": item.answer,
        "normalized_gold_answer": normalize_gold_answer(item),
        "correct": False,
        "parse_status": "invalid",
        "parser_name": "runtime_failure",
        "error_type": f"runtime_exception:{type(exc).__name__}",
        "exception_message": str(exc),
        "prompt_preview": "",
    }



def _compute_metrics(per_item_results: Iterable[dict]) -> dict[str, float | int]:
    results = list(per_item_results)
    total = len(results)
    correct = sum(1 for record in results if record["correct"])
    invalid = sum(1 for record in results if record["parse_status"] != "parsed")
    parsed = total - invalid
    return {
        "accuracy": (correct / total) if total else 0.0,
        "format_failure_rate": (invalid / total) if total else 0.0,
        "parsed_count": parsed,
        "invalid_count": invalid,
    }
