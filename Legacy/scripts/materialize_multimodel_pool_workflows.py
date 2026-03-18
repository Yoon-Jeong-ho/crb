from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "configs" / "model_pool_registry.yaml"
SINGLE_TURN_OUT = ROOT / "configs" / "generated" / "multimodel_single_turn_pools"
FOLLOWUP_OUT = ROOT / "configs" / "generated" / "multimodel_pool_followups"

DATASETS: dict[str, dict[str, Any]] = {
    "gpqa": {
        "target": {
            "dataset_name": "gpqa",
            "adapter": "gpqa",
            "path": "Idavidrein/gpqa",
            "subset": "gpqa_main",
            "split": "train",
            "cache_dir": "data/cache/huggingface",
        },
        "final_answer_instruction": "If the question is multiple choice, output only the choice letter. End with exactly one final line `Answer: <final_answer>`.",
        "other_dataset_sources": ["mmlu"],
        "cross_domain_sources": ["gsm8k", "aime"],
    },
    "gsm8k": {
        "target": {
            "dataset_name": "gsm8k",
            "adapter": "gsm8k",
            "path": "openai/gsm8k",
            "subset": "main",
            "split": "test",
            "cache_dir": "data/cache/huggingface",
        },
        "final_answer_instruction": "For arithmetic questions, output only the final numeric answer. End with exactly one final line `Answer: <final_answer>`.",
        "other_dataset_sources": ["aime"],
        "cross_domain_sources": ["gpqa"],
    },
    "aime": {
        "target": {
            "dataset_name": "aime",
            "adapter": "aime",
            "path": "HuggingFaceH4/aime_2024",
            "split": "train",
            "cache_dir": "data/cache/huggingface",
        },
        "final_answer_instruction": "For AIME-style problems, output only the final integer answer. End with exactly one final line `Answer: <final_answer>`.",
        "other_dataset_sources": ["gsm8k"],
        "cross_domain_sources": ["gpqa"],
    },
    "mmlu": {
        "target": {
            "dataset_name": "mmlu",
            "adapter": "mmlu",
            "path": "cais/mmlu",
            "subset": "all",
            "split": "test",
            "cache_dir": "data/cache/huggingface",
        },
        "final_answer_instruction": "If the question is multiple choice, output only the choice letter. End with exactly one final line `Answer: <final_answer>`.",
        "other_dataset_sources": [],
        "cross_domain_sources": ["gsm8k", "aime", "gpqa"],
    },
}

K_VALUES = [2, 4, 8, 16]
POOL_LABELS = ["correct", "incorrect"]


def load_registry() -> dict[str, Any]:
    return yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))


def normalize_variant_name(value: Any) -> str:
    if isinstance(value, bool):
        return "on" if value else "off"
    return str(value)


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_single_turn_config(model: dict[str, Any], variant: dict[str, Any], dataset_name: str) -> dict[str, Any]:
    dataset = DATASETS[dataset_name]
    variant_name = normalize_variant_name(variant["name"])
    return {
        "experiment": {
            "name": f"{model['slug']}_{dataset_name}_single_turn_pool_thinking_{variant_name}",
            "seed": 42,
            "num_samples": None,
            "tags": [model["slug"], dataset_name, "single_turn_pool", f"thinking_{variant_name}"],
        },
        "model": {
            "engine": "vllm",
            "model_name": model["model_name"],
            "model_family": model["model_family"],
            "thinking_mode": variant["thinking_mode"],
            "trust_remote_code": True,
            "tensor_parallel_size": "auto",
            "dtype": "auto",
            "max_model_len": 16384,
            "gpu_memory_utilization": 0.9,
            "download_dir": "/mnt/raid6/aa007878/.cache/huggingface",
            "seed": 42,
            "chat_template_kwargs": {"enable_thinking": variant["enable_thinking"]},
        },
        "decoding": {
            "temperature": variant["temperature"],
            "top_p": variant["top_p"],
            "top_k": variant["top_k"],
            "min_p": 0.0,
            "max_tokens": variant["max_tokens"],
        },
        "prompt": {
            "system_prompt": "You are a precise evaluation assistant. Solve the problem and end with exactly one final line `Answer: <final_answer>`.",
            "final_answer_instruction": dataset["final_answer_instruction"],
            "history_answer_prefix": "Answer:",
            "use_canonical_history": True,
        },
        "runtime": {
            "output_root": "results",
            "log_dir": "logs",
            "manifest_dir": "results/manifests",
            "summary_csv": "results/summary/scoreboard.csv",
            "prediction_pool_root": f"results/pools/single_turn/{model['slug']}/thinking_{variant_name}",
            "resume": True,
            "skip_completed": True,
            "timeout_seconds": 300,
        },
        "evaluation": {
            "evaluation_mode": "single_turn",
            "history_mode": "oracle_history",
            "dummy_type": "same_domain",
            "k": 0,
            "manifest_k_values": [0],
            "target": deepcopy(dataset["target"]),
        },
    }


def build_pool_source(model_slug: str, variant_name: str, dataset_name: str, split: str, pool_label: str) -> dict[str, Any]:
    return {
        "dataset_name": dataset_name,
        "adapter": "single_turn_pool",
        "split": split,
        "pool_model_slug": model_slug,
        "pool_thinking_mode": variant_name,
        "pool_label": pool_label,
    }


def build_followup_config(
    model: dict[str, Any],
    variant: dict[str, Any],
    target_dataset_name: str,
    pool_label: str,
    dummy_type: str,
    k: int,
) -> dict[str, Any] | None:
    dataset = DATASETS[target_dataset_name]
    variant_name = normalize_variant_name(variant["name"])
    if dummy_type == "same_domain":
        source_names = [target_dataset_name]
    elif dummy_type == "same_domain_other_dataset":
        source_names = list(dataset["other_dataset_sources"])
        if not source_names:
            return None
    elif dummy_type == "cross_domain":
        source_names = list(dataset["cross_domain_sources"])
    else:
        raise ValueError(dummy_type)
    sources = [
        build_pool_source(model["slug"], variant_name, source_name, DATASETS[source_name]["target"]["split"], pool_label)
        for source_name in source_names
    ]
    config = build_single_turn_config(model, variant, target_dataset_name)
    config["experiment"]["name"] = (
        f"{model['slug']}_{target_dataset_name}_stored_{dummy_type}_{pool_label}_thinking_{variant_name}_k{k}"
    )
    config["experiment"]["tags"] = [
        model["slug"],
        target_dataset_name,
        "stored_history",
        dummy_type,
        pool_label,
        f"thinking_{variant_name}",
        f"k{k}",
    ]
    config["runtime"]["prediction_pool_root"] = None
    config["evaluation"]["evaluation_mode"] = "multi_turn"
    config["evaluation"]["history_mode"] = "stored_history"
    config["evaluation"]["dummy_type"] = dummy_type
    config["evaluation"]["k"] = k
    config["evaluation"]["manifest_k_values"] = [0, 2, 4, 8, 16]
    config["evaluation"]["dummy_sources"] = sources
    return config


def materialize() -> list[Path]:
    registry = load_registry()
    generated: list[Path] = []
    ensure_dir(SINGLE_TURN_OUT)
    ensure_dir(FOLLOWUP_OUT)

    for model in registry["models"]:
        if not model.get("enabled", False):
            continue
        for variant in model["thinking_variants"]:
            variant_name = normalize_variant_name(variant["name"])
            single_turn_dir = ensure_dir(SINGLE_TURN_OUT / model["slug"])
            followup_dir = ensure_dir(FOLLOWUP_OUT / model["slug"])
            for dataset_name in DATASETS:
                config = build_single_turn_config(model, variant, dataset_name)
                out = single_turn_dir / f"{dataset_name}__thinking_{variant_name}.yaml"
                out.write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True), encoding="utf-8")
                generated.append(out)
                for pool_label in POOL_LABELS:
                    for dummy_type in ["same_domain", "same_domain_other_dataset", "cross_domain"]:
                        for k in K_VALUES:
                            followup = build_followup_config(model, variant, dataset_name, pool_label, dummy_type, k)
                            if followup is None:
                                continue
                            out = followup_dir / f"{dataset_name}__{dummy_type}__{pool_label}__thinking_{variant_name}__k-{k}.yaml"
                            out.write_text(yaml.safe_dump(followup, sort_keys=False, allow_unicode=True), encoding="utf-8")
                            generated.append(out)
    return generated


def main() -> None:
    generated = materialize()
    for path in generated:
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
