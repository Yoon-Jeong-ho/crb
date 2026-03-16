#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

from tools._artifact_utils import ANALYSIS_ROOT, normalize_float


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_series(rows: list[dict[str, str]], metric: str, split_by: str) -> tuple[list[str], dict[str, list[str]]]:
    ks = sorted({row["k"] for row in rows}, key=lambda value: int(value))
    grouped: dict[str, dict[str, float]] = defaultdict(dict)
    for row in rows:
        grouped[row[split_by]][row["k"]] = normalize_float(row[metric])
    return ks, {label: [f"{grouped[label].get(k, 0.0):.4f}" for k in ks] for label in sorted(grouped)}


def write_mermaid(path: Path, title: str, xs: list[str], series: dict[str, list[str]], metric: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# {title}",
        "",
        "```mermaid",
        "xychart-beta",
        f'    title "{title}"',
        f"    x-axis [{', '.join(xs)}]",
        f'    y-axis "{metric}" 0 --> 1',
    ]
    for label, values in series.items():
        lines.append(f'    line "{label}" [{", ".join(values)}]')
    lines.append("```")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a lightweight Mermaid plot from grouped CRB summary tables.")
    parser.add_argument("--input", default=str(ANALYSIS_ROOT / "tables" / "summary_table.csv"))
    parser.add_argument("--metric", default="avg_accuracy", choices=["avg_accuracy", "avg_format_failure_rate"])
    parser.add_argument("--split-by", default="dataset")
    parser.add_argument("--output", default=str(ANALYSIS_ROOT / "figures" / "metric_plot.md"))
    args = parser.parse_args()

    rows = load_rows(Path(args.input))
    xs, series = build_series(rows, args.metric, args.split_by)
    title = f"CRB {args.metric} by k split by {args.split_by}"
    write_mermaid(Path(args.output), title, xs, series, args.metric)
    print(f"wrote Mermaid plot to {args.output}")


if __name__ == "__main__":
    main()
