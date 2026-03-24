from __future__ import annotations

import time
from pathlib import Path

from crb_v2.artifacts import baseline_dir, pool_dir, sweep_dir
from crb_v2.benchmarks import create_adapter
from crb_v2.budget import fit_history_to_budget
from crb_v2.config import ModelConfig, PipelineConfig
from crb_v2.engines.base import InferenceEngine
from crb_v2.failures import INSUFFICIENT_DUMMY_POOL, summarize_reason_codes
from crb_v2.io import append_jsonl, read_json, read_jsonl, write_json
from crb_v2.run_utils import TimeoutException, timeout
from crb_v2.types import HistoryTurn, NormalizedExample, RunItemRecord, to_dict
from crb_v2.utils import choose_model_context_limit, utc_timestamp



def run_sweeps_for_model(*, config: PipelineConfig, experiment_root: Path, model: ModelConfig, engine: InferenceEngine) -> dict[str, dict]:
    summaries: dict[str, dict] = {}
    max_context_tokens = choose_model_context_limit(model.max_context_tokens, engine.tokenizer_model_limit)
    source_lookup = _source_lookup(experiment_root, model.key)
    for benchmark in config.benchmarks:
        adapter = create_adapter(benchmark)
        baseline_rows = read_jsonl(baseline_dir(experiment_root, model.key, benchmark.key) / "items.jsonl")
        combo_summaries: dict[str, dict] = {}
        for relation in config.sweep.relations:
            for provenance in config.sweep.provenances:
                manifest = read_json(pool_dir(experiment_root, model.key, benchmark.key) / relation / f"{provenance}.json")
                manifest_lookup = {entry["target_example_id"]: entry for entry in manifest["entries"]}
                for k in [value for value in config.sweep.k_values if value > 0]:
                    out_dir = sweep_dir(experiment_root, model.key, benchmark.key, relation, provenance, k)
                    summary_path = out_dir / "summary.json"
                    items_path = out_dir / "items.jsonl"
                    if summary_path.exists() and config.output.resume:
                        combo_summaries[f"{relation}:{provenance}:k{k}"] = read_json(summary_path)
                        continue
                    if items_path.exists() and config.output.overwrite:
                        items_path.unlink()
                    rows: list[dict] = []
                    for baseline_row in baseline_rows:
                        entry = manifest_lookup[baseline_row["example_id"]]
                        dummy_ids = entry["ordered_dummy_ids"][:k]
                        dummy_benchmarks = entry["ordered_dummy_benchmarks"][:k]
                        if len(dummy_ids) < k:
                            row = to_dict(RunItemRecord(
                                model_key=model.key,
                                benchmark_name=benchmark.key,
                                split=baseline_row["split"],
                                example_id=baseline_row["example_id"],
                                stage="sweep",
                                relation=relation,
                                provenance=provenance,
                                requested_k=k,
                                effective_k=len(dummy_ids),
                                seed=config.runtime.seed,
                                prompt_style=config.sweep.prompt_style,
                                prompt_token_count=None,
                                completion_token_count=None,
                                reason_codes=[INSUFFICIENT_DUMMY_POOL],
                                raw_output="",
                                parsed_answer=None,
                                parse_status="invalid",
                                parser_name=None,
                                normalized_gold_answer=baseline_row["normalized_gold_answer"],
                                scoreable=baseline_row["scoreable"],
                                is_correct=False,
                                prompt_text_path=None,
                                metadata={"available_dummy_count": len(dummy_ids)},
                            ))
                            rows.append(row)
                            append_jsonl(items_path, row)
                            continue
                        example = _baseline_row_to_example(benchmark.key, baseline_row)
                        history = [
                            HistoryTurn(
                                source_example_id=dummy_id,
                                benchmark_name=dummy_benchmark,
                                question=source_lookup[dummy_benchmark][dummy_id]["question"],
                                choices=source_lookup[dummy_benchmark][dummy_id].get("choices"),
                                answer=source_lookup[dummy_benchmark][dummy_id]["answer"],
                                provenance=provenance,  # type: ignore[arg-type]
                                source_domain=source_lookup[dummy_benchmark][dummy_id]["domain"],
                                source_subdomain=source_lookup[dummy_benchmark][dummy_id].get("subdomain"),
                            )
                            for dummy_id, dummy_benchmark in zip(dummy_ids, dummy_benchmarks)
                        ]
                        budget = fit_history_to_budget(
                            example=example,
                            history=history,
                            engine=engine,
                            max_context_tokens=max_context_tokens,
                            max_new_tokens=model.max_new_tokens,
                            system_prompt=config.sweep.system_prompt,
                            final_answer_instruction=config.sweep.final_answer_instruction,
                            history_answer_prefix=config.sweep.history_answer_prefix,
                            compaction_policy=config.sweep.compaction_policy,
                        )
                        reason_codes = list(budget.reason_codes)
                        raw_output = ""
                        score = adapter.score_prediction(example, raw_output)
                        if budget.prompt_text is not None:
                            try:
                                with timeout(config.runtime.timeout_seconds):
                                    raw_output = engine.generate(budget.prompt_text, request_options=_request_options(example))
                            except TimeoutException:
                                reason_codes.append("runtime_timeout")
                            except Exception as exc:  # noqa: BLE001
                                reason_codes.append("runtime_exception")
                                raw_output = f"[runtime_exception] {exc}"
                            score = adapter.score_prediction(example, raw_output)
                            if score.parse.reason_code:
                                reason_codes.append(score.parse.reason_code)
                        row = to_dict(RunItemRecord(
                            model_key=model.key,
                            benchmark_name=benchmark.key,
                            split=baseline_row["split"],
                            example_id=baseline_row["example_id"],
                            stage="sweep",
                            relation=relation,
                            provenance=provenance,
                            requested_k=k,
                            effective_k=len(budget.effective_history),
                            seed=config.runtime.seed,
                            prompt_style=config.sweep.prompt_style,
                            prompt_token_count=budget.prompt_token_count,
                            completion_token_count=None,
                            reason_codes=reason_codes,
                            raw_output=raw_output,
                            parsed_answer=score.parse.normalized_answer,
                            parse_status=score.parse.status,
                            parser_name=score.parse.parser_name,
                            normalized_gold_answer=score.normalized_gold_answer,
                            scoreable=score.scoreable,
                            is_correct=score.is_correct,
                            prompt_text_path=None,
                            metadata={
                                "requested_dummy_ids": dummy_ids,
                                "effective_dummy_ids": [turn.source_example_id for turn in budget.effective_history],
                            },
                        ))
                        rows.append(row)
                        append_jsonl(items_path, row)
                    summary = _build_summary(model.key, benchmark.key, relation, provenance, k, rows)
                    write_json(summary_path, summary)
                    combo_summaries[f"{relation}:{provenance}:k{k}"] = summary
                    if config.sweep.sleep_between_runs_seconds:
                        time.sleep(config.sweep.sleep_between_runs_seconds)
        summaries[benchmark.key] = combo_summaries
    return summaries



def _source_lookup(experiment_root: Path, model_key: str) -> dict[str, dict[str, dict]]:
    lookup: dict[str, dict[str, dict]] = {}
    for oracle_path in (experiment_root / "baseline" / model_key).glob("*/oracle_pool.jsonl"):
        benchmark = oracle_path.parent.name
        rows: dict[str, dict] = {}
        for pool_name in ["correct_pool.jsonl", "incorrect_pool.jsonl", "oracle_pool.jsonl"]:
            for row in read_jsonl(oracle_path.parent / pool_name):
                rows[row["example_id"]] = row
        lookup[benchmark] = rows
    return lookup



def _baseline_row_to_example(benchmark_name: str, row: dict) -> NormalizedExample:
    meta = row["metadata"]
    return NormalizedExample(
        benchmark_name=benchmark_name,
        split=row["split"],
        example_id=row["example_id"],
        domain=meta["domain"],
        subdomain=meta.get("subdomain"),
        question=meta["question"],
        choices=meta.get("choices"),
        gold_answer=meta["gold_answer"],
        benchmark_type=meta["benchmark_type"],
        metadata=meta,
    )



def _request_options(example: NormalizedExample) -> dict:
    if example.benchmark_type in {"multiple_choice", "completion_choice"}:
        return {"structured_choice": [chr(ord("A") + idx) for idx in range(len(example.choices or []))]}
    if example.benchmark_type == "yes_no":
        return {"structured_choice": ["yes", "no"]}
    return {}



def _build_summary(model_key: str, benchmark_key: str, relation: str, provenance: str, k: int, rows: list[dict]) -> dict:
    num_items = len(rows)
    valid_count = sum(1 for row in rows if row["parse_status"] == "parsed" and row["scoreable"] and not row["reason_codes"])
    correct_count = sum(1 for row in rows if row["is_correct"] and row["parse_status"] == "parsed" and not row["reason_codes"])
    parse_failure_count = 0
    format_failure_count = 0
    skipped_count = 0
    for row in rows:
        summary = summarize_reason_codes(row["reason_codes"])
        parse_failure_count += int(summary.parse_failure)
        format_failure_count += int(summary.format_failure)
        skipped_count += int(summary.skipped)
    return {
        "timestamp": utc_timestamp(),
        "model_key": model_key,
        "benchmark_name": benchmark_key,
        "stage": "sweep",
        "relation": relation,
        "provenance": provenance,
        "k": k,
        "num_items": num_items,
        "valid_answer_count": valid_count,
        "correct_count": correct_count,
        "parse_failure_count": parse_failure_count,
        "format_failure_count": format_failure_count,
        "skipped_count": skipped_count,
        "valid_answer_rate": (valid_count / num_items) if num_items else 0.0,
        "accuracy": (correct_count / valid_count) if valid_count else 0.0,
    }
