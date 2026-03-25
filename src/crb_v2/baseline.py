from __future__ import annotations

from pathlib import Path

from crb_v2.artifacts import baseline_dir
from crb_v2.benchmarks import create_adapter
from crb_v2.config import BenchmarkConfig, ModelConfig, PipelineConfig
from crb_v2.engines.base import InferenceEngine
from crb_v2.failures import eligible_for_correct_pool, eligible_for_incorrect_pool, summarize_reason_codes
from crb_v2.io import append_jsonl, read_json, write_json, write_jsonl
from crb_v2.run_utils import TimeoutException, timeout
from crb_v2.types import NormalizedExample, PoolRecord, RunItemRecord, to_dict
from crb_v2.utils import utc_timestamp



def run_baseline_for_model(*, config: PipelineConfig, experiment_root: Path, model: ModelConfig, engine: InferenceEngine) -> dict[str, dict]:
    return {
        benchmark.key: run_baseline_for_benchmark(
            config=config,
            experiment_root=experiment_root,
            model=model,
            benchmark_config=benchmark,
            engine=engine,
        )
        for benchmark in config.benchmarks
    }



def run_baseline_for_benchmark(*, config: PipelineConfig, experiment_root: Path, model: ModelConfig, benchmark_config: BenchmarkConfig, engine: InferenceEngine) -> dict:
    adapter = create_adapter(benchmark_config)
    out_dir = baseline_dir(experiment_root, model.key, benchmark_config.key)
    summary_path = out_dir / "summary.json"
    items_path = out_dir / "items.jsonl"
    if summary_path.exists() and config.output.resume:
        return read_json(summary_path)
    if items_path.exists() and config.output.overwrite:
        items_path.unlink()

    examples = adapter.load_examples()
    results: list[dict] = []
    correct_pool: list[dict] = []
    incorrect_pool: list[dict] = []
    oracle_pool: list[dict] = []
    correct_count = 0
    incorrect_count = 0
    completed_reason = "full_benchmark"

    for idx, example in enumerate(examples):
        if config.runtime.baseline_max_examples is not None and idx >= config.runtime.baseline_max_examples:
            completed_reason = "baseline_max_examples"
            break
        prompt_text = adapter.format_single_turn_prompt(
            example,
            system_prompt=config.sweep.system_prompt,
            final_answer_instruction=_final_answer_instruction(example, config),
        )
        reason_codes: list[str] = []
        raw_output = ""
        try:
            with timeout(config.runtime.timeout_seconds):
                raw_output = engine.generate(prompt_text, request_options=_request_options(example))
        except TimeoutException:
            reason_codes.append("runtime_timeout")
        except Exception as exc:  # noqa: BLE001
            reason_codes.append("runtime_exception")
            raw_output = f"[runtime_exception] {exc}"
        score = adapter.score_prediction(example, raw_output)
        if score.parse.reason_code:
            reason_codes.append(score.parse.reason_code)
        item = RunItemRecord(
            model_key=model.key,
            benchmark_name=benchmark_config.key,
            split=example.split,
            example_id=example.example_id,
            stage="baseline",
            relation="baseline",
            provenance="baseline",
            requested_k=0,
            effective_k=0,
            seed=config.runtime.seed,
            prompt_style=config.sweep.prompt_style,
            prompt_token_count=engine.count_tokens(prompt_text),
            completion_token_count=None,
            reason_codes=reason_codes,
            raw_output=raw_output,
            parsed_answer=score.parse.normalized_answer,
            parse_status=score.parse.status,
            parser_name=score.parse.parser_name,
            normalized_gold_answer=score.normalized_gold_answer,
            scoreable=score.scoreable,
            is_correct=score.is_correct,
            prompt_text_path=str(_write_prompt(out_dir, example.example_id, prompt_text)) if config.output.write_prompts else None,
            metadata={
                "domain": example.domain,
                "subdomain": example.subdomain,
                "question": example.question,
                "choices": example.choices,
                "gold_answer": example.gold_answer,
                "benchmark_type": example.benchmark_type,
            },
        )
        row = to_dict(item)
        results.append(row)
        append_jsonl(items_path, row)

        if eligible_for_correct_pool(score.parse.status, score.scoreable, score.is_correct, reason_codes):
            correct_count += 1
            correct_pool.append(_pool_record(model.key, benchmark_config.key, example, score.parse.normalized_answer or "", "model_correct", str(items_path)))
        elif eligible_for_incorrect_pool(score.parse.status, score.scoreable, score.is_correct, reason_codes):
            incorrect_count += 1
            incorrect_pool.append(_pool_record(model.key, benchmark_config.key, example, score.parse.normalized_answer or "", "model_incorrect", str(items_path)))
        oracle_pool.append(_pool_record(None, benchmark_config.key, example, adapter.normalize_gold_answer(example) or example.gold_answer, "oracle", None))

        if (
            not config.pool_policy.require_full_benchmark
            and correct_count >= config.pool_policy.min_correct
            and incorrect_count >= config.pool_policy.min_incorrect
        ):
            completed_reason = "min_pool_targets_reached"
            break

    write_jsonl(out_dir / "correct_pool.jsonl", correct_pool)
    write_jsonl(out_dir / "incorrect_pool.jsonl", incorrect_pool)
    write_jsonl(out_dir / "oracle_pool.jsonl", oracle_pool)
    summary = _build_summary(model.key, benchmark_config.key, results, len(examples), completed_reason)
    write_json(summary_path, summary)
    return summary



def _write_prompt(out_dir: Path, example_id: str, prompt_text: str) -> Path:
    prompt_dir = out_dir / "prompts"
    prompt_dir.mkdir(parents=True, exist_ok=True)
    target = prompt_dir / f"{example_id.replace('/', '__')}.txt"
    target.write_text(prompt_text, encoding="utf-8")
    return target



def _pool_record(model_key: str | None, benchmark_key: str, example: NormalizedExample, answer: str, provenance: str, source_result_path: str | None) -> dict:
    return to_dict(
        PoolRecord(
            benchmark_name=example.benchmark_name,
            split=example.split,
            example_id=example.example_id,
            domain=example.domain,
            subdomain=example.subdomain,
            question=example.question,
            choices=example.choices,
            answer=answer,
            provenance=provenance,  # type: ignore[arg-type]
            source_model_key=model_key,
            source_benchmark_name=benchmark_key,
            source_result_path=source_result_path,
            metadata={"gold_answer": example.gold_answer, "benchmark_type": example.benchmark_type},
        )
    )



def _request_options(example: NormalizedExample) -> dict:
    if example.benchmark_type in {"multiple_choice", "completion_choice"}:
        return {"structured_choice": [chr(ord("A") + idx) for idx in range(len(example.choices or []))]}
    if example.benchmark_type == "yes_no":
        return {"structured_choice": ["yes", "no"]}
    if example.benchmark_type == "numeric_boxed":
        return {"structured_regex": r"Answer:\s*\\boxed\{[-+]?\d+(?:\.\d+)?(?:/\d+)?\}"}
    return {}


def _final_answer_instruction(example: NormalizedExample, config: PipelineConfig) -> str:
    if example.benchmark_type in {"multiple_choice", "completion_choice"}:
        return "End with exactly one final line in the form `Answer: <LETTER>`."
    if example.benchmark_type == "yes_no":
        return "End with exactly one final line in the form `Answer: yes` or `Answer: no`."
    if example.benchmark_type == "numeric_boxed":
        return "End with exactly one final line in the form `Answer: \\boxed{<number>}`."
    return config.sweep.final_answer_instruction



def _build_summary(model_key: str, benchmark_key: str, rows: list[dict], total_available: int, completed_reason: str) -> dict:
    num_items = len(rows)
    valid_count = sum(1 for row in rows if row["parse_status"] == "parsed" and row["scoreable"] and not row["reason_codes"])
    correct_count = sum(1 for row in rows if row["is_correct"] and row["parse_status"] == "parsed" and not row["reason_codes"])
    incorrect_count = sum(1 for row in rows if row["parse_status"] == "parsed" and row["scoreable"] and not row["is_correct"] and not row["reason_codes"])
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
        "stage": "baseline",
        "num_items": num_items,
        "total_available_examples": total_available,
        "valid_answer_count": valid_count,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "parse_failure_count": parse_failure_count,
        "format_failure_count": format_failure_count,
        "skipped_count": skipped_count,
        "valid_answer_rate": (valid_count / num_items) if num_items else 0.0,
        "accuracy": (correct_count / valid_count) if valid_count else 0.0,
        "completed_reason": completed_reason,
    }
