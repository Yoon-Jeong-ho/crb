from __future__ import annotations

from abc import ABC, abstractmethod


class InferenceEngine(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError

    def close(self) -> None:
        return None
