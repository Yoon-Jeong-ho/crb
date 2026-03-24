from __future__ import annotations

from pathlib import Path

from crb_v2.artifacts import aggregate_dir
from crb_v2.config import PipelineConfig
from crb_v2.io import read_json, write_csv



def aggregate_results(*, config: PipelineConfig, experiment_root: Path) -> dict[str, str]:
    out_dir = aggregate_dir(experiment_root)
    baseline_rows = [read_json(path) for path in (experiment_root / "baseline").glob("*/*/summary.json")]
    sweep_rows = [read_json(path) for path in (experiment_root / "sweep").glob("*/*/*/*/summary.json")]
    baseline_index = {(row["model_key"], row["benchmark_name"]): row for row in baseline_rows}
    combined: list[dict] = []
    for row in baseline_rows:
        combined.append({
            "model_key": row["model_key"],
            "benchmark_name": row["benchmark_name"],
            "stage": "baseline",
            "relation": "baseline",
            "provenance": "baseline",
            "k": 0,
            "num_items": row["num_items"],
            "accuracy": row["accuracy"],
            "valid_answer_rate": row["valid_answer_rate"],
            "parse_failure_rate": row["parse_failure_count"] / row["num_items"] if row["num_items"] else 0.0,
            "format_failure_rate": row["format_failure_count"] / row["num_items"] if row["num_items"] else 0.0,
            "skipped_rate": row["skipped_count"] / row["num_items"] if row["num_items"] else 0.0,
            "delta_vs_k0": 0.0,
        })
    for row in sweep_rows:
        base = baseline_index[(row["model_key"], row["benchmark_name"])]
        combined.append({
            "model_key": row["model_key"],
            "benchmark_name": row["benchmark_name"],
            "stage": "sweep",
            "relation": row["relation"],
            "provenance": row["provenance"],
            "k": row["k"],
            "num_items": row["num_items"],
            "accuracy": row["accuracy"],
            "valid_answer_rate": row["valid_answer_rate"],
            "parse_failure_rate": row["parse_failure_count"] / row["num_items"] if row["num_items"] else 0.0,
            "format_failure_rate": row["format_failure_count"] / row["num_items"] if row["num_items"] else 0.0,
            "skipped_rate": row["skipped_count"] / row["num_items"] if row["num_items"] else 0.0,
            "delta_vs_k0": row["accuracy"] - base["accuracy"],
        })
    fields = ["model_key", "benchmark_name", "stage", "relation", "provenance", "k", "num_items", "accuracy", "valid_answer_rate", "parse_failure_rate", "format_failure_rate", "skipped_rate", "delta_vs_k0"]
    write_csv(out_dir / "summary_rows.csv", combined, fields)
    by_group = _group_summary(combined)
    write_csv(out_dir / "summary_by_group.csv", by_group, list(by_group[0].keys()) if by_group else ["model_key", "benchmark_name", "relation", "provenance", "rows", "avg_accuracy", "avg_delta_vs_k0"])
    (out_dir / "summary.md").write_text(_render_markdown(combined, by_group), encoding="utf-8")
    return {"summary_rows_csv": str(out_dir / "summary_rows.csv"), "summary_by_group_csv": str(out_dir / "summary_by_group.csv"), "summary_md": str(out_dir / "summary.md")}



def _group_summary(rows: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str, str, str], list[dict]] = {}
    for row in rows:
        grouped.setdefault((row["model_key"], row["benchmark_name"], row["relation"], row["provenance"]), []).append(row)
    result = []
    for key, bucket in sorted(grouped.items()):
        model_key, benchmark_name, relation, provenance = key
        result.append({
            "model_key": model_key,
            "benchmark_name": benchmark_name,
            "relation": relation,
            "provenance": provenance,
            "rows": len(bucket),
            "avg_accuracy": sum(row["accuracy"] for row in bucket) / len(bucket),
            "avg_delta_vs_k0": sum(row["delta_vs_k0"] for row in bucket) / len(bucket),
        })
    return result



def _render_markdown(rows: list[dict], groups: list[dict]) -> str:
    lines = ["# CRB v2 Aggregate Summary", "", f"- rows: {len(rows)}", "", "| model | benchmark | relation | provenance | rows | avg accuracy | avg delta vs k0 |", "| --- | --- | --- | --- | ---: | ---: | ---: |"]
    for row in groups:
        lines.append(f"| {row['model_key']} | {row['benchmark_name']} | {row['relation']} | {row['provenance']} | {row['rows']} | {row['avg_accuracy']:.4f} | {row['avg_delta_vs_k0']:.4f} |")
    return "\n".join(lines) + "\n"
