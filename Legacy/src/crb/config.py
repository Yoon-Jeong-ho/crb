from __future__ import annotations

from dataclasses import fields
from pathlib import Path
from typing import Any, TypeVar

import yaml

from crb.schemas import (
    DataSourceConfig,
    DecodingConfig,
    EvaluationConfig,
    ExperimentConfig,
    ModelConfig,
    PromptConfig,
    RunConfig,
    RuntimeConfig,
)

T = TypeVar("T")


class ConfigError(ValueError):
    """Raised when a YAML config cannot be parsed into the CRB schema."""


def _coerce_scalar(cls: type[T], name: str, value: Any) -> Any:
    if cls is ModelConfig and name == "thinking_mode" and isinstance(value, bool):
        return "on" if value else "off"
    return value


def _coerce_dataclass(cls: type[T], raw: dict[str, Any]) -> T:
    kwargs: dict[str, Any] = {}
    field_map = {field.name: field for field in fields(cls)}
    for name in raw:
        if name not in field_map:
            raise ConfigError(f"Unknown field `{name}` for {cls.__name__}")
    for name, field_def in field_map.items():
        if name not in raw:
            continue
        value = raw[name]
        if cls is EvaluationConfig and name == "target":
            kwargs[name] = _coerce_dataclass(DataSourceConfig, value)
        elif cls is EvaluationConfig and name == "dummy_sources":
            kwargs[name] = [_coerce_dataclass(DataSourceConfig, item) for item in value]
        else:
            kwargs[name] = _coerce_scalar(cls, name, value)
    return cls(**kwargs)


def load_run_config(path: str | Path) -> RunConfig:
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    if not isinstance(raw, dict):
        raise ConfigError("Top-level YAML document must be a mapping")

    required_sections = ["experiment", "model", "decoding", "prompt", "runtime", "evaluation"]
    missing = [section for section in required_sections if section not in raw]
    if missing:
        raise ConfigError(f"Missing top-level sections: {', '.join(missing)}")

    config = RunConfig(
        experiment=_coerce_dataclass(ExperimentConfig, raw["experiment"]),
        model=_coerce_dataclass(ModelConfig, raw["model"]),
        decoding=_coerce_dataclass(DecodingConfig, raw["decoding"]),
        prompt=_coerce_dataclass(PromptConfig, raw["prompt"]),
        runtime=_coerce_dataclass(RuntimeConfig, raw["runtime"]),
        evaluation=_coerce_dataclass(EvaluationConfig, raw["evaluation"]),
    )
    if config.evaluation.k not in config.evaluation.manifest_k_values:
        raise ConfigError(
            f"evaluation.k={config.evaluation.k} must appear in evaluation.manifest_k_values"
        )
    if config.prompt.target_thinking_mode not in {"default", "think", "no_think"}:
        raise ConfigError(
            "prompt.target_thinking_mode must be one of: default, think, no_think"
        )
    if config.decoding.target_structured_choice and config.decoding.target_structured_regex:
        raise ConfigError(
            "Set only one of decoding.target_structured_choice or decoding.target_structured_regex"
        )
    if config.decoding.target_choice_from_item_choices and config.decoding.target_structured_choice:
        raise ConfigError(
            "Use either decoding.target_choice_from_item_choices or decoding.target_structured_choice, not both"
        )
    return config
