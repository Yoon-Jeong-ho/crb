from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class InferenceEngine(ABC):
    @abstractmethod
    def generate(self, prompt: str, request_options: dict[str, Any] | None = None) -> str:
        raise NotImplementedError

    def close(self) -> None:
        return None
