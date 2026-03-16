#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

from tools._artifact_utils import ANALYSIS_ROOT, normalize_float, normalize_int, write_csv, write_markdown_table


def load_inventory(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_summary(rows: list[dict[str, str]], group_by: list[str]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row[field] for field in group_by)].append(row)

    output: list[dict[str, object]] = []
    for key, group in sorted(grouped.items()):
        row = {field: value for field, value in zip(group_by, key, strict=True)}
        row["runs"] = len(group)
        row["avg_accuracy"] = round(sum(normalize_float(item["accuracy"]) for item in group) / len(group), 6)
        row["avg_format_failure_rate"] = round(
            sum(normalize_float(item["format_failure_rate"]) for item in group) / len(group), 6
        )
        row["total_items"] = sum(normalize_int(item["num_items"]) for item in group)
        output.append(row)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Build grouped CRB summary tables from the aggregated inventory.")
    parser.add_argument("--inventory", default=str(ANALYSIS_ROOT / "tables" / "run_inventory.csv"))
    parser.add_argument("--group-by", default="dataset,evaluation_mode,history_mode,dummy_type,k,thinking_mode")
    parser.add_argument("--output-prefix", default=str(ANALYSIS_ROOT / "tables" / "summary_table"))
    args = parser.parse_args()

    rows = load_inventory(Path(args.inventory))
    group_by = [field.strip() for field in args.group_by.split(",") if field.strip()]
    summary_rows = build_summary(rows, group_by)

    csv_path = Path(f"{args.output_prefix}.csv")
    md_path = Path(f"{args.output_prefix}.md")
    fieldnames = [*group_by, "runs", "avg_accuracy", "avg_format_failure_rate", "total_items"]
    write_csv(csv_path, summary_rows, fieldnames)
    write_markdown_table(md_path, "CRB Summary Table", summary_rows, fieldnames)
    print(f"wrote {len(summary_rows)} grouped rows to {csv_path} and {md_path}")


if __name__ == "__main__":
    main()
