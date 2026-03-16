#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from tools._artifact_utils import ANALYSIS_ROOT, LEGACY_ROOT, read_scoreboard_rows, safe_load_run_payload, write_csv


def build_inventory() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in read_scoreboard_rows():
        result_path = LEGACY_ROOT / row["result_json_path"]
        payload = safe_load_run_payload(result_path)
        metrics = (payload or {}).get("metrics", {})
        rows.append(
            {
                **row,
                "result_json_path_abs": str(result_path.resolve()),
                "run_dir": str(result_path.parent.resolve()),
                "manifest_path": (payload or {}).get("manifest_path", ""),
                "parsed_count": metrics.get("parsed_count", ""),
                "invalid_count": metrics.get("invalid_count", ""),
                "result_json_exists": result_path.exists(),
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate CRB scoreboard + run JSON metadata into one inventory table.")
    parser.add_argument("--output", default=str(ANALYSIS_ROOT / "tables" / "run_inventory.csv"))
    args = parser.parse_args()

    rows = build_inventory()
    fieldnames = [
        "timestamp",
        "run_id",
        "git_commit",
        "model_name",
        "model_family",
        "thinking_mode",
        "dataset",
        "split",
        "evaluation_mode",
        "history_mode",
        "dummy_type",
        "k",
        "seed",
        "num_items",
        "accuracy",
        "format_failure_rate",
        "parsed_count",
        "invalid_count",
        "manifest_path",
        "result_json_path",
        "result_json_path_abs",
        "run_dir",
        "result_json_exists",
    ]
    write_csv(Path(args.output), rows, fieldnames)
    print(f"wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
