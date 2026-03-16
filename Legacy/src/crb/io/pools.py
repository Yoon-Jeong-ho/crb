from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from crb.io.results import read_jsonl, write_json
from crb.utils.runtime import ensure_parent


def export_single_turn_run_to_prediction_pool(
    *,
    payload: dict[str, Any],
    output_root: str | Path,
    source_result_json_path: str | Path,
) -> dict[str, Any]:
    root = Path(output_root)
    per_item_results = list(payload.get("per_item_results", []))
    source_result_json_path = str(Path(source_result_json_path))

    grouped_source_records: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    grouped_valid_records: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    all_valid_records: list[dict[str, Any]] = []

    for record in per_item_results:
        dataset_name = str(record["dataset_name"])
        split = str(record["split"])
        grouped_source_records[(dataset_name, split)].append(record)
        if not _is_format_valid(record):
            continue
        pool_record = _build_pool_record(
            payload=payload,
            item_record=record,
            source_result_json_path=source_result_json_path,
        )
        grouped_valid_records[(dataset_name, split)].append(pool_record)
        all_valid_records.append(pool_record)

    overall_summary = _build_summary(
        payload=payload,
        source_records=per_item_results,
        valid_records=all_valid_records,
        bucket_dataset_name="all_datasets",
        bucket_split="all",
    )
    _merge_bucket(
        bucket_dir=root / "all_datasets",
        records=all_valid_records,
        summary=overall_summary,
    )
    write_json(root / "latest_run_summary.json", overall_summary)

    dataset_summaries: dict[str, dict[str, Any]] = {}
    for (dataset_name, split), source_records in grouped_source_records.items():
        valid_records = grouped_valid_records[(dataset_name, split)]
        summary = _build_summary(
            payload=payload,
            source_records=source_records,
            valid_records=valid_records,
            bucket_dataset_name=dataset_name,
            bucket_split=split,
        )
        _merge_bucket(
            bucket_dir=root / dataset_name / split,
            records=valid_records,
            summary=summary,
        )
        dataset_summaries[f"{dataset_name}:{split}"] = summary

    write_json(
        root / "latest_dataset_summaries.json",
        {"run_id": payload["run_id"], "datasets": dataset_summaries},
    )
    return overall_summary


def _is_format_valid(record: dict[str, Any]) -> bool:
    parsed_answer = record.get("parsed_answer")
    return record.get("parse_status") == "parsed" and parsed_answer not in (None, "")


def _build_pool_record(
    *,
    payload: dict[str, Any],
    item_record: dict[str, Any],
    source_result_json_path: str,
) -> dict[str, Any]:
    answer_type = item_record.get("answer_type")
    if answer_type is None:
        answer_type = "mcq" if item_record.get("choices") else "numeric"
    return {
        "dataset_name": item_record["dataset_name"],
        "split": item_record["split"],
        "item_id": item_record["item_id"],
        "domain": item_record.get("domain"),
        "subject": item_record.get("subject"),
        "question": item_record["question"],
        "choices": item_record.get("choices"),
        "answer": item_record["parsed_answer"],
        "answer_type": answer_type,
        "source_correct": bool(item_record["correct"]),
        "source_model_name": payload["model_name"],
        "source_model_family": payload["model_family"],
        "source_thinking_mode": payload["thinking_mode"],
        "source_run_id": payload["run_id"],
        "source_result_json_path": source_result_json_path,
        "source_evaluation_mode": payload["evaluation_mode"],
        "source_gold_answer": item_record.get("normalized_gold_answer"),
        "source_raw_output": item_record.get("raw_output"),
        "source_parser_name": item_record.get("parser_name"),
        "source_generation_controls": item_record.get("generation_controls"),
    }


def _build_summary(
    *,
    payload: dict[str, Any],
    source_records: list[dict[str, Any]],
    valid_records: list[dict[str, Any]],
    bucket_dataset_name: str,
    bucket_split: str,
) -> dict[str, Any]:
    correct_count = sum(1 for record in valid_records if record["source_correct"])
    incorrect_count = len(valid_records) - correct_count
    invalid_count = len(source_records) - len(valid_records)
    return {
        "run_id": payload["run_id"],
        "timestamp": payload["timestamp"],
        "model_name": payload["model_name"],
        "model_family": payload["model_family"],
        "thinking_mode": payload["thinking_mode"],
        "evaluation_mode": payload["evaluation_mode"],
        "dataset_name": bucket_dataset_name,
        "split": bucket_split,
        "total_items": len(source_records),
        "format_valid_items": len(valid_records),
        "format_invalid_items": invalid_count,
        "correct_items": correct_count,
        "incorrect_items": incorrect_count,
    }


def _merge_bucket(
    *,
    bucket_dir: Path,
    records: list[dict[str, Any]],
    summary: dict[str, Any],
) -> None:
    correct_path = bucket_dir / "correct.jsonl"
    incorrect_path = bucket_dir / "incorrect.jsonl"
    correct_map = _load_bucket_map(correct_path)
    incorrect_map = _load_bucket_map(incorrect_path)

    for record in records:
        item_id = str(record["item_id"])
        correct_map.pop(item_id, None)
        incorrect_map.pop(item_id, None)
        if record["source_correct"]:
            correct_map[item_id] = record
        else:
            incorrect_map[item_id] = record

    _write_jsonl(correct_path, correct_map.values())
    _write_jsonl(incorrect_path, incorrect_map.values())

    summary_payload = dict(summary)
    summary_payload["pool_correct_items"] = len(correct_map)
    summary_payload["pool_incorrect_items"] = len(incorrect_map)
    summary_payload["correct_path"] = str(correct_path)
    summary_payload["incorrect_path"] = str(incorrect_path)
    write_json(bucket_dir / "summary.json", summary_payload)


def _load_bucket_map(path: Path) -> dict[str, dict[str, Any]]:
    return {str(record["item_id"]): record for record in read_jsonl(path)}


def _write_jsonl(path: str | Path, records: Any) -> None:
    target = ensure_parent(path)
    with target.open("w", encoding="utf-8") as handle:
        for record in sorted(records, key=lambda item: str(item["item_id"])):
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
