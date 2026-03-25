from __future__ import annotations

from crb_v2.benchmarks.adapters import (
    ArcChallengeAdapter,
    BoolQAdapter,
    FixtureMCQAdapter,
    FixtureNumericAdapter,
    GPQAAdapter,
    GSM8KAdapter,
    HellaSwagAdapter,
    MATH500Adapter,
    MMLUProAdapter,
    MMLUReduxAdapter,
    PIQAAdapter,
    TruthfulQAMCAdapter,
)
from crb_v2.catalog import BENCHMARK_SPECS, MODEL_SPECS
from crb_v2.config import BenchmarkConfig, ModelConfig

ADAPTERS = {
    "gsm8k": GSM8KAdapter,
    "math500": MATH500Adapter,
    "gpqa": GPQAAdapter,
    "arc_challenge": ArcChallengeAdapter,
    "mmlu_pro": MMLUProAdapter,
    "mmlu_redux_2": MMLUReduxAdapter,
    "hellaswag": HellaSwagAdapter,
    "piqa": PIQAAdapter,
    "boolq": BoolQAdapter,
    "truthfulqa_mc": TruthfulQAMCAdapter,
    "fixture_mcq": FixtureMCQAdapter,
    "fixture_numeric": FixtureNumericAdapter,
}


def resolve_model_config(config: ModelConfig) -> ModelConfig:
    spec = MODEL_SPECS.get(config.key)
    if spec is None:
        return config
    if config.model_name is None:
        config.model_name = spec.model_name
    if config.max_context_tokens is None:
        config.max_context_tokens = spec.max_context_tokens
    return config


def resolve_benchmark_config(config: BenchmarkConfig) -> BenchmarkConfig:
    spec = BENCHMARK_SPECS.get(config.key)
    if spec is None:
        raise KeyError(f"Unknown benchmark key: {config.key}")
    if config.path is None:
        config.path = spec.path
    if config.subset is None:
        config.subset = spec.subset
    if config.split is None:
        config.split = spec.split
    if config.key == "piqa":
        config.trust_remote_code = True
    return config


def create_adapter(config: BenchmarkConfig):
    resolved = resolve_benchmark_config(config)
    adapter_cls = ADAPTERS[resolved.key]
    return adapter_cls(resolved)
