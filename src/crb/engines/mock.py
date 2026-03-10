from __future__ import annotations

import re

from crb.engines.base import InferenceEngine


class MockEngine(InferenceEngine):
    def generate(self, prompt: str) -> str:
        letter_match = re.search(r"Correct answer:\s*([A-J])", prompt)
        if letter_match:
            return f"Answer: {letter_match.group(1)}"
        numeric_match = re.search(r"Correct answer:\s*([-+]?\d+(?:/\d+)?)", prompt)
        if numeric_match:
            return f"Answer: {numeric_match.group(1)}"
        option_match = re.findall(r"\b([A-D])\. ", prompt)
        if option_match:
            return "Answer: A"
        number_match = re.findall(r"(-?\d+)", prompt)
        if number_match:
            return f"Answer: {number_match[-1]}"
        return "Answer: [invalid]"
