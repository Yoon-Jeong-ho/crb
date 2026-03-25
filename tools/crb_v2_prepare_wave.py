from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import yaml

from crb_v2.catalog import BENCHMARK_SPECS, MODEL_SPECS

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_TABLES = ROOT / "analysis_v2" / "tables"
RESULT_MANIFESTS = ROOT / "results_v2" / "manifests"
RESULT_SUMMARY = ROOT / "results_v2" / "summary"
GENERATED_CONFIGS = ROOT / "configs_v2" / "generated"

MODELS: list[str] = [
    "qwen25_7b_instruct",
    "llama31_8b_instruct",
    "mistral7b_instruct_v03",
    "gemma2_9b_it",
    "phi4_mini_instruct",
    "mistral_small_24b_instruct_2501",
    "deepseek_r1_distill_qwen_7b",
    "deepseek_r1_distill_llama_8b",
    "qwq_32b",
    "olmo2_1124_7b_instruct",
]

BENCHMARKS: list[str] = [
    "gsm8k",
    "math500",
    "gpqa",
    "arc_challenge",
    "mmlu_pro",
    "mmlu_redux_2",
    "hellaswag",
    "piqa",
    "boolq",
    "truthfulqa_mc",
]

K_VALUES_FULL = [0, 1, 2, 4, 8, 16, 32]
K_VALUES_SMOKE = [0, 2, 8]
RELATIONS = ["same_benchmark", "same_domain_other_benchmark", "cross_domain"]
SAMPLE_TYPES = ["model_correct", "model_incorrect"]

SMOKE_MODELS = ["qwen25_7b_instruct", "llama31_8b_instruct"]
SMOKE_BENCHMARKS = ["gsm8k", "gpqa"]
PILOT_MODELS = [
    "qwen25_7b_instruct",
    "llama31_8b_instruct",
    "phi4_mini_instruct",
    "deepseek_r1_distill_qwen_7b",
]
PILOT_BENCHMARKS = ["gsm8k", "math500", "gpqa", "arc_challenge"]

MODEL_NOTES: dict[str, dict[str, str | int]] = {
    "qwen25_7b_instruct": {
        "family": "qwen25",
        "model_type": "instruct",
        "size_class": "small",
        "preferred_tp": 1,
        "status": "ready",
        "execution_bucket": "bulk_ready",
        "evidence": "results_v2/pilot_qwen_llama_gsm8k_boolq_fix1__37025e5ec2b31c81 + results_v2/crb_v2_full__qwen25_7b_instruct__b212faf67c7cae2a",
    },
    "llama31_8b_instruct": {
        "family": "llama31",
        "model_type": "instruct",
        "size_class": "small",
        "preferred_tp": 1,
        "status": "ready",
        "execution_bucket": "bulk_ready",
        "evidence": "results_v2/pilot_qwen_llama_gsm8k_boolq_fix1__37025e5ec2b31c81 + results_v2/crb_v2_full__llama31_8b_instruct__d79d4f0349d597a0",
    },
    "mistral7b_instruct_v03": {
        "family": "mistral7b",
        "model_type": "instruct",
        "size_class": "small",
        "preferred_tp": 1,
        "status": "ready",
        "execution_bucket": "bulk_ready",
        "evidence": "results_v2/crb_v2_full__mistral7b_instruct_v03__e6693e0117c31aae",
    },
    "gemma2_9b_it": {
        "family": "gemma2",
        "model_type": "instruct",
        "size_class": "small",
        "preferred_tp": 1,
        "status": "blocked",
        "execution_bucket": "retry_blocked",
        "evidence": "logs/crb_v2_full_gpu6_20260324T140712Z.log + logs/crb_v2_full_gpu4_20260324T140712Z.log",
    },
    "phi4_mini_instruct": {
        "family": "phi4",
        "model_type": "instruct",
        "size_class": "small",
        "preferred_tp": 1,
        "status": "ready",
        "execution_bucket": "bulk_ready",
        "evidence": "results_v2/crb_v2_full__phi4_mini_instruct__5849c095fdc7ff30/pipeline_result.json",
    },
    "mistral_small_24b_instruct_2501": {
        "family": "mistral_small",
        "model_type": "instruct",
        "size_class": "medium",
        "preferred_tp": 2,
        "status": "ready",
        "execution_bucket": "retry_tp2",
        "evidence": "results_v2/crb_v2_full__mistral_small_24b_instruct_2501__030ab7ccbdac9afc",
    },
    "deepseek_r1_distill_qwen_7b": {
        "family": "deepseek_r1_distill_qwen",
        "model_type": "reasoning",
        "size_class": "small",
        "preferred_tp": 1,
        "status": "ready",
        "execution_bucket": "bulk_ready",
        "evidence": "results_v2/crb_v2_full__deepseek_r1_distill_qwen_7b__6c51e3ee9175b54c",
    },
    "deepseek_r1_distill_llama_8b": {
        "family": "deepseek_r1_distill_llama",
        "model_type": "reasoning",
        "size_class": "small",
        "preferred_tp": 1,
        "status": "ready",
        "execution_bucket": "bulk_unverified",
        "evidence": "src/crb_v2/catalog.py + configs_v2/full/full_matrix.yaml (runtime artifact not yet present)",
    },
    "qwq_32b": {
        "family": "qwq",
        "model_type": "reasoning",
        "size_class": "large",
        "preferred_tp": 2,
        "status": "ready",
        "execution_bucket": "retry_tp2",
        "evidence": "results_v2/crb_v2_full__qwq_32b__0d2c0cd3d77df2f8",
    },
    "olmo2_1124_7b_instruct": {
        "family": "olmo2",
        "model_type": "instruct",
        "size_class": "small",
        "preferred_tp": 1,
        "status": "ready",
        "execution_bucket": "bulk_unverified",
        "evidence": "src/crb_v2/catalog.py + results_v2/crb_v2_full__olmo2_1124_7b_instruct__1bb113a6877ee620/resolved_config.json",
    },
}

BENCHMARK_NOTES: dict[str, dict[str, str]] = {
    "gsm8k": {"status": "ready", "evidence": "adapter load check 2026-03-25 + catalog/adapter present"},
    "math500": {"status": "ready", "evidence": "adapter load check 2026-03-25 + catalog/adapter present"},
    "gpqa": {"status": "ready", "evidence": "adapter load check 2026-03-25 + subset gpqa_main in src/crb_v2/catalog.py"},
    "arc_challenge": {"status": "ready", "evidence": "adapter load check 2026-03-25 + catalog/adapter present"},
    "mmlu_pro": {"status": "ready", "evidence": "adapter load check 2026-03-25 + catalog/adapter present"},
    "mmlu_redux_2": {"status": "ready", "evidence": "adapter load check 2026-03-25 + recursive subset loader present"},
    "hellaswag": {"status": "ready", "evidence": "adapter load check 2026-03-25 + catalog/adapter present"},
    "piqa": {"status": "ready", "evidence": "adapter load check 2026-03-25 + trust_remote_code enabled in registry"},
    "boolq": {"status": "ready", "evidence": "adapter load check 2026-03-25 + pilot artifact exists"},
    "truthfulqa_mc": {"status": "ready", "evidence": "adapter load check 2026-03-25 + catalog/adapter present"},
}


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")


def model_config(model_key: str) -> dict[str, Any]:
    meta = MODEL_NOTES[model_key]
    config: dict[str, Any] = {
        "key": model_key,
        "tensor_parallel_size": int(meta["preferred_tp"]),
    }
    if meta["model_type"] == "reasoning":
        config["max_new_tokens"] = 192
    else:
        config["max_new_tokens"] = 128
    return config


def benchmark_config(benchmark_key: str, limit: int | None = None) -> dict[str, Any]:
    spec = BENCHMARK_SPECS[benchmark_key]
    payload: dict[str, Any] = {"key": benchmark_key, "split": spec.split}
    if limit is not None:
        payload["limit"] = limit
    return payload


def build_pipeline_config(
    *,
    experiment_name: str,
    models: list[str],
    benchmarks: list[str],
    k_values: list[int],
    benchmark_limit: int | None,
    min_correct: int,
    min_incorrect: int,
) -> dict[str, Any]:
    return {
        "experiment_name": experiment_name,
        "models": [model_config(model) for model in models],
        "benchmarks": [benchmark_config(benchmark, benchmark_limit) for benchmark in benchmarks],
        "pool_policy": {
            "require_full_benchmark": False,
            "min_correct": min_correct,
            "min_incorrect": min_incorrect,
        },
        "sweep": {
            "k_values": k_values,
            "relations": RELATIONS,
            "provenances": SAMPLE_TYPES,
        },
        "output": {"root_dir": "results_v2", "overwrite": False, "resume": True},
        "runtime": {"seed": 42, "timeout_seconds": 180},
    }


def scan_existing_runs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for run_dir in sorted(path for path in (ROOT / "results_v2").iterdir() if path.is_dir()):
        resolved_config = run_dir / "resolved_config.json"
        config = json.loads(resolved_config.read_text(encoding="utf-8")) if resolved_config.exists() else {}
        models = [model["key"] for model in config.get("models", [])]
        benchmarks = [benchmark["key"] for benchmark in config.get("benchmarks", [])]
        has_baseline = (run_dir / "baseline").exists()
        has_pools = (run_dir / "pools").exists()
        has_sweep = (run_dir / "sweep").exists()
        has_aggregate = (run_dir / "aggregate").exists()
        has_pipeline_result = (run_dir / "pipeline_result.json").exists()
        status = "complete" if has_aggregate and has_pipeline_result else "partial" if any([has_baseline, has_pools, has_sweep]) else "config_only"
        rows.append(
            {
                "run_name": run_dir.name,
                "experiment_name": config.get("experiment_name", ""),
                "model_count": len(models),
                "benchmark_count": len(benchmarks),
                "models": "|".join(models),
                "benchmarks": "|".join(benchmarks),
                "has_baseline": has_baseline,
                "has_pools": has_pools,
                "has_sweep": has_sweep,
                "has_aggregate": has_aggregate,
                "has_pipeline_result": has_pipeline_result,
                "status": status,
                "path": str(run_dir.relative_to(ROOT)),
            }
        )
    return rows


def build_model_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model_key in MODELS:
        spec = MODEL_SPECS[model_key]
        note = MODEL_NOTES[model_key]
        rows.append(
            {
                "model_key": model_key,
                "hf_model_name": spec.model_name,
                "family": note["family"],
                "model_type": note["model_type"],
                "size_class": note["size_class"],
                "preferred_tp": note["preferred_tp"],
                "status": note["status"],
                "execution_bucket": note["execution_bucket"],
                "evidence": note["evidence"],
            }
        )
    return rows


def build_benchmark_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for benchmark_key in BENCHMARKS:
        spec = BENCHMARK_SPECS[benchmark_key]
        note = BENCHMARK_NOTES[benchmark_key]
        rows.append(
            {
                "benchmark_key": benchmark_key,
                "domain": spec.domain,
                "benchmark_type": spec.benchmark_type,
                "hf_path": spec.path,
                "subset": spec.subset,
                "split": spec.split,
                "status": note["status"],
                "evidence": note["evidence"],
            }
        )
    return rows


def build_readiness_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model_key in MODELS:
        for benchmark_key in BENCHMARKS:
            status = MODEL_NOTES[model_key]["status"]
            detail = MODEL_NOTES[model_key]["evidence"]
            if BENCHMARK_NOTES[benchmark_key]["status"] != "ready":
                status = BENCHMARK_NOTES[benchmark_key]["status"]
                detail = BENCHMARK_NOTES[benchmark_key]["evidence"]
            rows.append(
                {
                    "model_key": model_key,
                    "benchmark_key": benchmark_key,
                    "domain": BENCHMARK_SPECS[benchmark_key].domain,
                    "status": status,
                    "execution_bucket": MODEL_NOTES[model_key]["execution_bucket"],
                    "evidence": detail,
                }
            )
    return rows


def build_job_manifest() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    benchmark_domains = {key: BENCHMARK_SPECS[key].domain for key in BENCHMARKS}
    for model_key in MODELS:
        model_status = MODEL_NOTES[model_key]["status"]
        execution_bucket = MODEL_NOTES[model_key]["execution_bucket"]
        for benchmark_key in BENCHMARKS:
            for relation in RELATIONS:
                relation_available = True
                if relation == "same_domain_other_benchmark":
                    relation_available = any(
                        other != benchmark_key and benchmark_domains[other] == benchmark_domains[benchmark_key]
                        for other in BENCHMARKS
                    )
                elif relation == "cross_domain":
                    relation_available = any(
                        benchmark_domains[other] != benchmark_domains[benchmark_key] for other in BENCHMARKS
                    )
                for sample_type in SAMPLE_TYPES:
                    for k in K_VALUES_FULL:
                        planned_status = "queued"
                        if model_status == "blocked":
                            planned_status = "blocked"
                        elif not relation_available and k > 0:
                            planned_status = "blocked"
                        rows.append(
                            {
                                "model_key": model_key,
                                "benchmark_key": benchmark_key,
                                "domain": benchmark_domains[benchmark_key],
                                "sample_type": sample_type,
                                "relation": relation,
                                "k": k,
                                "tier": "tier1",
                                "planned_status": planned_status,
                                "execution_bucket": execution_bucket,
                            }
                        )
    return rows


def build_wave_rows(name: str, models: list[str], benchmarks: list[str], k_values: list[int]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    domains = {key: BENCHMARK_SPECS[key].domain for key in benchmarks}
    for model in models:
        for benchmark in benchmarks:
            for relation in RELATIONS:
                relation_available = True
                if relation == "same_domain_other_benchmark":
                    relation_available = any(other != benchmark and domains[other] == domains[benchmark] for other in benchmarks)
                elif relation == "cross_domain":
                    relation_available = any(domains[other] != domains[benchmark] for other in benchmarks)
                for sample_type in SAMPLE_TYPES:
                    rows.append(
                        {
                            "wave": name,
                            "model_key": model,
                            "benchmark_key": benchmark,
                            "relation": relation,
                            "relation_available": relation_available,
                            "sample_type": sample_type,
                            "k_values": "|".join(str(k) for k in k_values),
                        }
                    )
    return rows


def assign_bulk_queue(model_key: str) -> str:
    bucket = MODEL_NOTES[model_key]["execution_bucket"]
    if bucket == "bulk_ready":
        lane_a = {"qwen25_7b_instruct", "mistral7b_instruct_v03", "deepseek_r1_distill_qwen_7b"}
        return "gpu6_bulk" if model_key in lane_a else "gpu7_bulk"
    return "retry_queue"


def main() -> None:
    ANALYSIS_TABLES.mkdir(parents=True, exist_ok=True)
    RESULT_MANIFESTS.mkdir(parents=True, exist_ok=True)
    RESULT_SUMMARY.mkdir(parents=True, exist_ok=True)
    (ROOT / "logs" / "crb_v2" / "gpu4").mkdir(parents=True, exist_ok=True)
    (ROOT / "logs" / "crb_v2" / "gpu5").mkdir(parents=True, exist_ok=True)
    (ROOT / "logs" / "crb_v2" / "gpu6").mkdir(parents=True, exist_ok=True)
    (ROOT / "logs" / "crb_v2" / "gpu7").mkdir(parents=True, exist_ok=True)

    model_rows = build_model_rows()
    benchmark_rows = build_benchmark_rows()
    readiness_rows = build_readiness_rows()
    run_rows = scan_existing_runs()
    job_rows = build_job_manifest()
    smoke_rows = build_wave_rows("smoke", SMOKE_MODELS, SMOKE_BENCHMARKS, K_VALUES_SMOKE)
    pilot_rows = build_wave_rows("pilot", PILOT_MODELS, PILOT_BENCHMARKS, K_VALUES_FULL)

    smoke_config_paths: list[str] = []
    for model_key in SMOKE_MODELS:
        config_path = GENERATED_CONFIGS / "smoke" / f"{model_key}__gsm8k_gpqa.yaml"
        write_yaml(
            config_path,
            build_pipeline_config(
                experiment_name=f"crb_v2_smoke__{model_key}__gsm8k_gpqa",
                models=[model_key],
                benchmarks=SMOKE_BENCHMARKS,
                k_values=K_VALUES_SMOKE,
                benchmark_limit=16,
                min_correct=4,
                min_incorrect=4,
            ),
        )
        smoke_config_paths.append(str(config_path.relative_to(ROOT)))

    for model_key in PILOT_MODELS:
        write_yaml(
            GENERATED_CONFIGS / "pilot" / f"{model_key}__4x4.yaml",
            build_pipeline_config(
                experiment_name=f"crb_v2_pilot__{model_key}__4x4",
                models=[model_key],
                benchmarks=PILOT_BENCHMARKS,
                k_values=K_VALUES_FULL,
                benchmark_limit=32,
                min_correct=8,
                min_incorrect=8,
            ),
        )

    full_model_config_rows: list[dict[str, str]] = []
    for model_key in MODELS:
        config_path = GENERATED_CONFIGS / "full_models" / f"{model_key}.yaml"
        write_yaml(
            config_path,
            build_pipeline_config(
                experiment_name=f"crb_v2_full__{model_key}",
                models=[model_key],
                benchmarks=BENCHMARKS,
                k_values=K_VALUES_FULL,
                benchmark_limit=None,
                min_correct=50,
                min_incorrect=50,
            ),
        )
        full_model_config_rows.append(
            {
                "model_key": model_key,
                "config_path": str(config_path.relative_to(ROOT)),
                "queue": assign_bulk_queue(model_key),
                "status": MODEL_NOTES[model_key]["status"],
                "execution_bucket": MODEL_NOTES[model_key]["execution_bucket"],
            }
        )

    queues = {
        "gpu4_smoke": [smoke_config_paths[0]],
        "gpu5_smoke": [smoke_config_paths[1]],
        "gpu6_bulk": [row["config_path"] for row in full_model_config_rows if row["queue"] == "gpu6_bulk"],
        "gpu7_bulk": [row["config_path"] for row in full_model_config_rows if row["queue"] == "gpu7_bulk"],
        "retry_queue": [row["config_path"] for row in full_model_config_rows if row["queue"] == "retry_queue"],
    }
    queue_dir = RESULT_MANIFESTS / "queues"
    queue_dir.mkdir(parents=True, exist_ok=True)
    for queue_name, paths in queues.items():
        (queue_dir / f"{queue_name}.txt").write_text("\n".join(paths) + ("\n" if paths else ""), encoding="utf-8")

    inventory_summary_rows = []
    existing_by_experiment = {row["experiment_name"]: row for row in run_rows}
    for row in full_model_config_rows:
        experiment_name = f"crb_v2_full__{row['model_key']}"
        existing = existing_by_experiment.get(experiment_name, {})
        inventory_summary_rows.append(
            {
                "model_key": row["model_key"],
                "status": row["status"],
                "execution_bucket": row["execution_bucket"],
                "config_path": row["config_path"],
                "existing_run_status": existing.get("status", "not_started"),
                "existing_run_path": existing.get("path", ""),
                "has_baseline": existing.get("has_baseline", False),
                "has_pools": existing.get("has_pools", False),
                "has_sweep": existing.get("has_sweep", False),
                "has_aggregate": existing.get("has_aggregate", False),
                "has_pipeline_result": existing.get("has_pipeline_result", False),
            }
        )

    manifest_payload = {
        "wave": "2026-03-25-v2-tier1",
        "models": MODELS,
        "benchmarks": BENCHMARKS,
        "k_values": K_VALUES_FULL,
        "relations": RELATIONS,
        "sample_types": SAMPLE_TYPES,
        "smoke": {"models": SMOKE_MODELS, "benchmarks": SMOKE_BENCHMARKS, "k_values": K_VALUES_SMOKE},
        "pilot": {"models": PILOT_MODELS, "benchmarks": PILOT_BENCHMARKS, "k_values": K_VALUES_FULL},
        "queues": {key: [value for value in values] for key, values in queues.items()},
    }
    (RESULT_MANIFESTS / "v2_experiment_inventory.json").write_text(json.dumps(manifest_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    write_csv(
        ANALYSIS_TABLES / "models_inventory.csv",
        model_rows,
        ["model_key", "hf_model_name", "family", "model_type", "size_class", "preferred_tp", "status", "execution_bucket", "evidence"],
    )
    write_csv(
        ANALYSIS_TABLES / "benchmarks_inventory.csv",
        benchmark_rows,
        ["benchmark_key", "domain", "benchmark_type", "hf_path", "subset", "split", "status", "evidence"],
    )
    write_csv(
        ANALYSIS_TABLES / "model_benchmark_readiness.csv",
        readiness_rows,
        ["model_key", "benchmark_key", "domain", "status", "execution_bucket", "evidence"],
    )
    write_csv(
        ANALYSIS_TABLES / "existing_run_inventory.csv",
        run_rows,
        ["run_name", "experiment_name", "model_count", "benchmark_count", "models", "benchmarks", "has_baseline", "has_pools", "has_sweep", "has_aggregate", "has_pipeline_result", "status", "path"],
    )
    write_csv(
        ANALYSIS_TABLES / "job_manifest_tier1.csv",
        job_rows,
        ["model_key", "benchmark_key", "domain", "sample_type", "relation", "k", "tier", "planned_status", "execution_bucket"],
    )
    write_csv(
        ANALYSIS_TABLES / "smoke_matrix.csv",
        smoke_rows,
        ["wave", "model_key", "benchmark_key", "relation", "relation_available", "sample_type", "k_values"],
    )
    write_csv(
        ANALYSIS_TABLES / "pilot_matrix.csv",
        pilot_rows,
        ["wave", "model_key", "benchmark_key", "relation", "relation_available", "sample_type", "k_values"],
    )
    write_csv(
        ANALYSIS_TABLES / "full_model_configs.csv",
        full_model_config_rows,
        ["model_key", "config_path", "queue", "status", "execution_bucket"],
    )
    write_csv(
        RESULT_SUMMARY / "inventory_summary.csv",
        inventory_summary_rows,
        ["model_key", "status", "execution_bucket", "config_path", "existing_run_status", "existing_run_path", "has_baseline", "has_pools", "has_sweep", "has_aggregate", "has_pipeline_result"],
    )

    print(json.dumps({
        "analysis_tables": [
            str((ANALYSIS_TABLES / "models_inventory.csv").relative_to(ROOT)),
            str((ANALYSIS_TABLES / "benchmarks_inventory.csv").relative_to(ROOT)),
            str((ANALYSIS_TABLES / "model_benchmark_readiness.csv").relative_to(ROOT)),
            str((ANALYSIS_TABLES / "existing_run_inventory.csv").relative_to(ROOT)),
            str((ANALYSIS_TABLES / "job_manifest_tier1.csv").relative_to(ROOT)),
            str((ANALYSIS_TABLES / "smoke_matrix.csv").relative_to(ROOT)),
            str((ANALYSIS_TABLES / "pilot_matrix.csv").relative_to(ROOT)),
            str((ANALYSIS_TABLES / "full_model_configs.csv").relative_to(ROOT)),
        ],
        "manifests": str((RESULT_MANIFESTS / "v2_experiment_inventory.json").relative_to(ROOT)),
        "summary": str((RESULT_SUMMARY / "inventory_summary.csv").relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
