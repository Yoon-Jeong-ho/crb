#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from typing import Any

from tools._artifact_utils import ANALYSIS_ROOT, normalize_float, normalize_int, write_csv


def load_inventory(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def pool_label_from_row(row: dict[str, str]) -> str:
    target = " ".join(
        [
            row.get("run_id", ""),
            row.get("result_json_path", ""),
            row.get("manifest_path", ""),
        ]
    ).lower()
    if "incorrect" in target:
        return "incorrect"
    if "correct" in target:
        return "correct"
    return ""


def latest_rows(rows: list[dict[str, str]], key_fields: list[str]) -> dict[tuple[str, ...], dict[str, str]]:
    latest: dict[tuple[str, ...], dict[str, str]] = {}
    for row in rows:
        key = tuple(row.get(field, "") for field in key_fields)
        latest[key] = row
    return latest


def baseline_map(rows: list[dict[str, str]]) -> dict[tuple[str, str, str], dict[str, str]]:
    baseline_rows = [
        row
        for row in rows
        if row.get("evaluation_mode") == "single_turn"
        and row.get("history_mode") == "oracle_history"
        and row.get("dummy_type") == "same_domain"
        and row.get("k") == "0"
        and str(row.get("result_json_exists", "")).lower() == "true"
    ]
    return latest_rows(baseline_rows, ["model_family", "dataset", "thinking_mode"])


def attach_common_fields(
    *,
    row: dict[str, str] | None,
    baseline: dict[str, str] | None,
    figure_slice: str,
    relation_label: str,
    provenance_label: str,
    status: str,
) -> dict[str, Any]:
    baseline_accuracy = normalize_float((baseline or {}).get("accuracy"))
    accuracy = normalize_float((row or {}).get("accuracy"))
    ff = normalize_float((row or {}).get("format_failure_rate"))
    baseline_ff = normalize_float((baseline or {}).get("format_failure_rate"))
    return {
        "figure_slice": figure_slice,
        "model_family": (row or baseline or {}).get("model_family", ""),
        "model_name": (row or baseline or {}).get("model_name", ""),
        "dataset": (row or baseline or {}).get("dataset", ""),
        "thinking_mode": (row or baseline or {}).get("thinking_mode", ""),
        "evaluation_mode": (row or {}).get("evaluation_mode", ""),
        "history_mode": (row or {}).get("history_mode", ""),
        "dummy_type": (row or {}).get("dummy_type", ""),
        "relation_label": relation_label,
        "provenance_label": provenance_label,
        "pool_label": pool_label_from_row(row or {}),
        "k": (row or {}).get("k", ""),
        "status": status,
        "baseline_run_id": (baseline or {}).get("run_id", ""),
        "baseline_accuracy": baseline_accuracy,
        "baseline_format_failure_rate": baseline_ff,
        "baseline_num_items": (baseline or {}).get("num_items", ""),
        "baseline_join_ok": bool(row and baseline and row.get("num_items") == baseline.get("num_items")),
        "run_id": (row or {}).get("run_id", ""),
        "num_items": (row or {}).get("num_items", ""),
        "accuracy": accuracy if row else "",
        "format_failure_rate": ff if row else "",
        "delta_vs_single_turn_k0": (accuracy - baseline_accuracy) if row and baseline else "",
        "ff_delta_vs_single_turn_k0": (ff - baseline_ff) if row and baseline else "",
        "result_json_path": (row or {}).get("result_json_path", ""),
    }


def build_main_table(rows: list[dict[str, str]], baselines: dict[tuple[str, str, str], dict[str, str]]) -> list[dict[str, Any]]:
    expected_models = ["qwen25", "llama", "mistral"]
    expected_datasets = ["gpqa", "gsm8k", "aime", "mmlu"]
    expected_pools = ["correct", "incorrect"]
    expected_ks = ["2", "4", "8", "16"]

    filtered = []
    for row in rows:
        if row.get("model_family") not in expected_models:
            continue
        if row.get("dataset") not in expected_datasets:
            continue
        if row.get("thinking_mode") != "off":
            continue
        if row.get("evaluation_mode") != "multi_turn":
            continue
        if row.get("history_mode") != "stored_history":
            continue
        if row.get("dummy_type") != "cross_domain":
            continue
        if not pool_label_from_row(row):
            continue
        baseline = baselines.get((row["model_family"], row["dataset"], row["thinking_mode"]))
        if baseline and row.get("num_items") == baseline.get("num_items"):
            filtered.append(row)

    latest = latest_rows(filtered, ["model_family", "dataset", "thinking_mode", "k", "result_json_path"])
    by_expected: dict[tuple[str, str, str, str], dict[str, str]] = {}
    for row in latest.values():
        key = (row["model_family"], row["dataset"], pool_label_from_row(row), row["k"])
        by_expected[key] = row

    output: list[dict[str, Any]] = []
    for model in expected_models:
        for dataset in expected_datasets:
            baseline = baselines.get((model, dataset, "off"))
            for pool in expected_pools:
                for k in expected_ks:
                    row = by_expected.get((model, dataset, pool, k))
                    status = "complete" if row and baseline else "missing"
                    output.append(
                        attach_common_fields(
                            row=row,
                            baseline=baseline,
                            figure_slice="main_multimodel_external_contamination",
                            relation_label="cross_domain",
                            provenance_label=f"stored_{pool}",
                            status=status,
                        )
                    )
                    output[-1]["pool_label"] = pool
                    output[-1]["k"] = k
    return output


def build_supporting_table(rows: list[dict[str, str]], baselines: dict[tuple[str, str, str], dict[str, str]]) -> list[dict[str, Any]]:
    expected = [
        ("oracle_history", "", "oracle"),
        ("wrong_history", "", "wrong"),
        ("stored_history", "correct", "stored_correct"),
        ("stored_history", "incorrect", "stored_incorrect"),
    ]
    expected_ks = ["2", "4", "8"]
    filtered = []
    for row in rows:
        if row.get("model_family") != "qwen3" or row.get("dataset") != "gpqa" or row.get("thinking_mode") != "off":
            continue
        if row.get("evaluation_mode") != "multi_turn" or row.get("dummy_type") != "same_domain":
            continue
        if row.get("history_mode") not in {"oracle_history", "wrong_history", "stored_history"}:
            continue
        baseline = baselines.get(("qwen3", "gpqa", "off"))
        if baseline and row.get("num_items") == baseline.get("num_items"):
            filtered.append(row)
    latest = latest_rows(filtered, ["history_mode", "k", "result_json_path"])
    indexed: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in latest.values():
        indexed[(row["history_mode"], pool_label_from_row(row), row["k"])] = row

    baseline = baselines.get(("qwen3", "gpqa", "off"))
    output: list[dict[str, Any]] = []
    for history_mode, pool, label in expected:
        for k in expected_ks:
            row = indexed.get((history_mode, pool, k))
            status = "complete" if row and baseline else "missing"
            output.append(
                attach_common_fields(
                    row=row,
                    baseline=baseline,
                    figure_slice="supporting_qwen3_gpqa_provenance",
                    relation_label="same_domain",
                    provenance_label=label,
                    status=status,
                )
            )
            output[-1]["pool_label"] = pool
            output[-1]["k"] = k
    return output


def build_appendix_table(rows: list[dict[str, str]], baselines: dict[tuple[str, str, str], dict[str, str]]) -> list[dict[str, Any]]:
    baseline = baselines.get(("qwen3", "gsm8k", "on"))
    expected_required = [
        ("self_history", "self", "0"),
        ("self_history", "self", "2"),
        ("self_history", "self", "4"),
        ("wrong_history", "wrong", "2"),
        ("wrong_history", "wrong", "4"),
        ("wrong_history", "wrong", "8"),
    ]
    expected_optional = [("self_history", "self", "8")]

    filtered = []
    for row in rows:
        if row.get("model_family") != "qwen3" or row.get("dataset") != "gsm8k" or row.get("thinking_mode") != "on":
            continue
        if row.get("evaluation_mode") != "single_turn_flattened" or row.get("dummy_type") != "cross_domain":
            continue
        if row.get("history_mode") not in {"self_history", "wrong_history"}:
            continue
        if row.get("num_items") in {"1319", baseline.get("num_items", "") if baseline else ""}:
            filtered.append(row)
    latest = latest_rows(filtered, ["history_mode", "k", "result_json_path"])
    indexed: dict[tuple[str, str], dict[str, str]] = {}
    for row in latest.values():
        if row.get("history_mode") == "wrong_history":
            indexed[("wrong", row["k"])] = row
        elif row.get("history_mode") == "self_history":
            indexed[("self", row["k"])] = row

    output: list[dict[str, Any]] = []
    for history_mode, label, k in expected_required + expected_optional:
        row = indexed.get((label, k))
        status = "complete" if row and baseline else "missing"
        required_for_figure = (history_mode, label, k) in expected_required
        if not required_for_figure and not row:
            status = "optional_missing"
        elif required_for_figure and not row:
            status = "pending_rerun"
        output.append(
            attach_common_fields(
                row=row,
                baseline=baseline,
                figure_slice="appendix_qwen3_gsm8k_self_vs_wrong",
                relation_label="cross_domain",
                provenance_label=label,
                status=status,
            )
        )
        output[-1]["pool_label"] = ""
        output[-1]["k"] = k
        output[-1]["required_for_figure"] = required_for_figure
    return output


def memo_for_table(title: str, rows: list[dict[str, Any]]) -> tuple[bool, list[str]]:
    required_rows = [row for row in rows if row.get("status") not in {"optional_missing"}]
    missing = [row for row in required_rows if row.get("status") != "complete"]
    baseline_fail = [row for row in required_rows if row.get("status") == "complete" and not row.get("baseline_join_ok")]
    ready = not missing and not baseline_fail
    lines = [f"## {title}", ""]
    lines.append(f"- rows: {len(rows)}")
    lines.append(f"- required rows: {len(required_rows)}")
    lines.append(f"- complete required rows: {sum(1 for row in required_rows if row.get('status') == 'complete')}")
    lines.append(f"- baseline join failures: {len(baseline_fail)}")
    lines.append(f"- figure-ready: {'YES' if ready else 'NO'}")
    if missing:
        lines.append("- missing / pending required cells:")
        for row in missing:
            lines.append(
                f"  - provenance={row.get('provenance_label')} model={row.get('model_family')} dataset={row.get('dataset')} k={row.get('k')} status={row.get('status')}"
            )
    if baseline_fail:
        lines.append("- baseline join failures:")
        for row in baseline_fail:
            lines.append(
                f"  - provenance={row.get('provenance_label')} model={row.get('model_family')} dataset={row.get('dataset')} k={row.get('k')}"
            )
    if not missing and not baseline_fail:
        lines.append("- no required gaps detected")
    lines.append("")
    return ready, lines


def write_figure_ready_memo(path: Path, main_rows: list[dict[str, Any]], supporting_rows: list[dict[str, Any]], appendix_rows: list[dict[str, Any]]) -> None:
    main_ready, main_lines = memo_for_table("Main: multimodel external contamination", main_rows)
    supporting_ready, supporting_lines = memo_for_table("Supporting: Qwen3 GPQA provenance", supporting_rows)
    appendix_ready, appendix_lines = memo_for_table("Appendix: Qwen3 GSM8K self-vs-wrong", appendix_rows)

    lines = [
        "# Figure Readiness Memo",
        "",
        "- Date: 2026-03-20",
        f"- Main figure ready: {'YES' if main_ready else 'NO'}",
        f"- Supporting figure ready: {'YES' if supporting_ready else 'NO'}",
        f"- Appendix figure ready now: {'YES' if appendix_ready else 'NO'}",
        "",
        "Appendix readiness rule used here:",
        "- required cells = self {0,2,4} and wrong {2,4,8}",
        "- optional later cell = self {8}",
        "",
    ]
    lines.extend(main_lines)
    lines.extend(supporting_lines)
    lines.extend(appendix_lines)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build claim-specific CRB slice tables and figure readiness memo.")
    parser.add_argument("--inventory", default=str(ANALYSIS_ROOT / "tables" / "run_inventory.csv"))
    args = parser.parse_args()

    rows = load_inventory(Path(args.inventory))
    baselines = baseline_map(rows)

    main_rows = build_main_table(rows, baselines)
    supporting_rows = build_supporting_table(rows, baselines)
    appendix_rows = build_appendix_table(rows, baselines)

    common_fields = [
        "figure_slice",
        "model_family",
        "model_name",
        "dataset",
        "thinking_mode",
        "evaluation_mode",
        "history_mode",
        "dummy_type",
        "relation_label",
        "provenance_label",
        "pool_label",
        "k",
        "status",
        "required_for_figure",
        "baseline_run_id",
        "baseline_accuracy",
        "baseline_format_failure_rate",
        "baseline_num_items",
        "baseline_join_ok",
        "run_id",
        "num_items",
        "accuracy",
        "format_failure_rate",
        "delta_vs_single_turn_k0",
        "ff_delta_vs_single_turn_k0",
        "result_json_path",
    ]

    write_csv(ANALYSIS_ROOT / "tables" / "main_multimodel_external_contamination.csv", main_rows, common_fields)
    write_csv(ANALYSIS_ROOT / "tables" / "supporting_qwen3_gpqa_provenance.csv", supporting_rows, common_fields)
    write_csv(ANALYSIS_ROOT / "tables" / "appendix_qwen3_gsm8k_self_vs_wrong.csv", appendix_rows, common_fields)
    write_figure_ready_memo(ANALYSIS_ROOT / "notes" / "figure_ready_20260320.md", main_rows, supporting_rows, appendix_rows)

    print("wrote:")
    print(ANALYSIS_ROOT / "tables" / "main_multimodel_external_contamination.csv")
    print(ANALYSIS_ROOT / "tables" / "supporting_qwen3_gpqa_provenance.csv")
    print(ANALYSIS_ROOT / "tables" / "appendix_qwen3_gsm8k_self_vs_wrong.csv")
    print(ANALYSIS_ROOT / "notes" / "figure_ready_20260320.md")


if __name__ == "__main__":
    main()
