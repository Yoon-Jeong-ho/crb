from __future__ import annotations

from crb.engines.base import InferenceEngine
from crb.engines.mock import MockEngine
from crb.schemas import RunConfig



def create_engine(config: RunConfig) -> InferenceEngine:
    if config.model.engine == "mock":
        return MockEngine()
    if config.model.engine == "vllm":
        from crb.engines.vllm_engine import VllmEngine

        return VllmEngine(config.model, config.decoding)
    raise ValueError(f"Unsupported engine: {config.model.engine}")
