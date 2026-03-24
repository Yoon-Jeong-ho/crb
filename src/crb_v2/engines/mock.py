from __future__ import annotations

import re
from typing import Any

from crb_v2.engines.base import InferenceEngine


class MockEngine(InferenceEngine):
    def generate(self, prompt: str, request_options: dict[str, Any] | None = None) -> str:
        request_options = request_options or {}
        structured_choice = request_options.get("structured_choice") or []
        if structured_choice:
            return f"Answer: {structured_choice[0]}"
        number_match = re.findall(r"(-?\d+(?:/\d+)?)", prompt)
        if number_match:
            return f"Answer: \\boxed{{{number_match[-1]}}}"
        yn = re.findall(r"\b(yes|no)\b", prompt, flags=re.IGNORECASE)
        if yn:
            return f"Answer: {yn[-1].lower()}"
        return "Answer: mock"

    def count_tokens(self, prompt: str) -> int:
        return len(prompt.split())
