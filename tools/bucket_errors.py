#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from tools._artifact_utils import ANALYSIS_ROOT, LEGACY_ROOT, read_scoreboard_rows, safe_load_run_payload, write_csv, write_markdown_table


def classify_error(item: dict[str, object]) -> str:
    error_type = str(item.get("error_type") or "")
    raw_output = str(item.get("raw_output") or "")
    lowered = raw_output.lower()
    if "letter_output_for_numeric" in error_type:
        return "letter_output_for_numeric"
    if "no_final" in error_type or "no final" in lowered:
        return "no_final_answer"
    if "multiple" in error_type or lowered.count("answer:") > 1:
        return "multiple_answers"
    if "numeric" in error_type:
        return "malformed_numeric"
    if "answer:" not in lowered:
        return "no_final_answer"
    if any(token in lowered for token in ["because", "therefore", "let's", "reasoning"]):
        return "reasoning_only_or_malformed_final"
    return "other_invalid"


def build_rows(dataset_filter: str | None = None) -> list[dict[str, object]]:
    counts: Counter[tuple[str, str, str]] = Counter()
    for row in read_scoreboard_rows():
        if dataset_filter and row["dataset"] != dataset_filter:
            continue
        payload = safe_load_run_payload(LEGACY_ROOT / row["result_json_path"])
        if payload is None:
            counts[(row["dataset"], row["run_id"], "missing_result_json")] += 1
            continue
        for item in payload.get("per_item_results", []):
            if item.get("parse_status") == "parsed":
                continue
            counts[(row["dataset"], row["run_id"], classify_error(item))] += 1
    return [
        {"dataset": dataset, "run_id": run_id, "error_bucket": bucket, "count": count}
        for (dataset, run_id, bucket), count in sorted(counts.items())
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Bucket invalid CRB outputs from run JSONs.")
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--output-prefix", default=str(ANALYSIS_ROOT / "error_buckets" / "error_buckets"))
    args = parser.parse_args()

    rows = build_rows(args.dataset)
    csv_path = Path(f"{args.output_prefix}.csv")
    md_path = Path(f"{args.output_prefix}.md")
    fieldnames = ["dataset", "run_id", "error_bucket", "count"]
    write_csv(csv_path, rows, fieldnames)
    write_markdown_table(md_path, "CRB Error Buckets", rows, fieldnames)
    print(f"wrote {len(rows)} error rows to {csv_path} and {md_path}")


if __name__ == "__main__":
    main()
