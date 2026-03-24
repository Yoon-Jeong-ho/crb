from __future__ import annotations

from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any, TypeVar

import yaml

from crb_v2.types import PromptStyle, ProvenanceType, RelationType

T = TypeVar("T")


class ConfigError(ValueError):
    pass


@dataclass(slots=True)
class ModelConfig:
    key: str
    model_name: str | None = None
    engine: str = "vllm"
    trust_remote_code: bool = True
    tensor_parallel_size: int | str = "auto"
    dtype: str = "auto"
    max_context_tokens: int | None = None
    gpu_memory_utilization: float = 0.9
    download_dir: str | None = None
    enforce_eager: bool = False
    swap_space: float = 4.0
    max_num_seqs: int | None = None
    seed: int = 42
    temperature: float = 0.0
    top_p: float = 1.0
    top_k: int = -1
    min_p: float = 0.0
    max_new_tokens: int = 256
    repetition_penalty: float = 1.0
    presence_penalty: float = 0.0
    stop: list[str] = field(default_factory=list)


@dataclass(slots=True)
class BenchmarkConfig:
    key: str
    split: str | None = None
    path: str | None = None
    subset: str | None = None
    local_path: str | None = None
    limit: int | None = None
    shuffle: bool = False
    seed: int = 42
    trust_remote_code: bool = False
    cache_dir: str | None = None
    extra_kwargs: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class PoolPolicyConfig:
    require_full_benchmark: bool = False
    min_correct: int = 50
    min_incorrect: int = 50


@dataclass(slots=True)
class SweepConfig:
    k_values: list[int] = field(default_factory=lambda: [0, 2, 4, 8, 16, 32])
    relations: list[RelationType] = field(default_factory=lambda: ["same_benchmark", "same_domain_other_benchmark", "cross_domain"])
    provenances: list[ProvenanceType] = field(default_factory=lambda: ["model_correct", "model_incorrect", "oracle"])
    prompt_style: PromptStyle = "flat"
    system_prompt: str = "You are a precise evaluation assistant. Solve the problem and end with exactly one final answer line."
    final_answer_instruction: str = "End with exactly one final line in the form `Answer: <final_answer>`."
    history_answer_prefix: str = "Answer:"
    compaction_policy: str = "drop_oldest_history"
    sleep_between_runs_seconds: int = 0


@dataclass(slots=True)
class OutputConfig:
    root_dir: str = "results_v2"
    overwrite: bool = False
    resume: bool = True
    write_prompts: bool = True


@dataclass(slots=True)
class RuntimeConfig:
    seed: int = 42
    timeout_seconds: int | None = None
    baseline_max_examples: int | None = None
    pilot_allow_underfilled_pools: bool = False


@dataclass(slots=True)
class PipelineConfig:
    experiment_name: str
    models: list[ModelConfig]
    benchmarks: list[BenchmarkConfig]
    pool_policy: PoolPolicyConfig = field(default_factory=PoolPolicyConfig)
    sweep: SweepConfig = field(default_factory=SweepConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    runtime: RuntimeConfig = field(default_factory=RuntimeConfig)



def _coerce_dataclass(cls: type[T], raw: dict[str, Any]) -> T:
    known = {field.name for field in fields(cls)}
    unknown = [name for name in raw if name not in known]
    if unknown:
        raise ConfigError(f"Unknown field(s) for {cls.__name__}: {', '.join(sorted(unknown))}")
    kwargs: dict[str, Any] = {}
    for field_def in fields(cls):
        name = field_def.name
        if name not in raw:
            continue
        value = raw[name]
        if cls is PipelineConfig and name == "models":
            kwargs[name] = [_coerce_dataclass(ModelConfig, item) for item in value]
        elif cls is PipelineConfig and name == "benchmarks":
            kwargs[name] = [_coerce_dataclass(BenchmarkConfig, item) for item in value]
        elif cls is PipelineConfig and name == "pool_policy":
            kwargs[name] = _coerce_dataclass(PoolPolicyConfig, value)
        elif cls is PipelineConfig and name == "sweep":
            kwargs[name] = _coerce_dataclass(SweepConfig, value)
        elif cls is PipelineConfig and name == "output":
            kwargs[name] = _coerce_dataclass(OutputConfig, value)
        elif cls is PipelineConfig and name == "runtime":
            kwargs[name] = _coerce_dataclass(RuntimeConfig, value)
        else:
            kwargs[name] = value
    return cls(**kwargs)



def load_pipeline_config(path: str | Path) -> PipelineConfig:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ConfigError("Top-level config must be a mapping")
    config = _coerce_dataclass(PipelineConfig, raw)
    if not config.models:
        raise ConfigError("At least one model must be configured")
    if not config.benchmarks:
        raise ConfigError("At least one benchmark must be configured")
    if sorted(set(config.sweep.k_values)) != config.sweep.k_values:
        raise ConfigError("sweep.k_values must be sorted and unique")
    if 0 not in config.sweep.k_values:
        raise ConfigError("sweep.k_values must include 0")
    return config
