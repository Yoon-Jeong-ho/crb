from __future__ import annotations

from crb_v2.catalog import MODEL_SPECS
from crb_v2.config import ModelConfig
from crb_v2.engines.base import InferenceEngine
from crb_v2.engines.mock import MockEngine
from crb_v2.engines.vllm import VllmEngine



def resolve_model_config(config: ModelConfig) -> ModelConfig:
    spec = MODEL_SPECS.get(config.key)
    if spec and config.model_name is None:
        config.model_name = spec.model_name
    if spec and config.max_context_tokens is None:
        config.max_context_tokens = spec.max_context_tokens
    return config



def create_engine(config: ModelConfig) -> InferenceEngine:
    config = resolve_model_config(config)
    if config.engine == "mock":
        return MockEngine()
    if config.engine == "vllm":
        if not config.model_name:
            raise ValueError(f"Model config {config.key} requires model_name when engine=vllm")
        return VllmEngine(config)
    raise ValueError(f"Unsupported engine: {config.engine}")
