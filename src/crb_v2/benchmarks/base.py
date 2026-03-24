from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from pathlib import Path
from typing import Any

from datasets import load_dataset

from crb_v2.config import BenchmarkConfig
from crb_v2.failures import (
    BOXED_MISSING,
    CONFLICTING_FINAL_ANSWERS,
    EMPTY_OUTPUT,
    INVALID_OPTION_CHOICE,
    PARSE_FAILURE,
    UNSUPPORTED_BENCHMARK_TYPE,
)
from crb_v2.prompts import build_multi_turn_prompt, build_single_turn_prompt
from crb_v2.types import HistoryTurn, NormalizedExample, ParseResult, ScoreResult

ANSWER_LINE_RE = re.compile(r"Answer\s*:\s*(.+)", re.IGNORECASE)
LETTER_RE = re.compile(r"\b([A-J])\b")
BOXED_RE = re.compile(r"\\boxed\{([^{}]+)\}")
NUMERIC_RE = re.compile(r"[-+]?\d+(?:\.\d+)?(?:/\d+)?")
YESNO_RE = re.compile(r"\b(yes|no)\b", re.IGNORECASE)


class BenchmarkAdapter(ABC):
    benchmark_name: str
    domain: str
    benchmark_type: str

    def __init__(self, config: BenchmarkConfig) -> None:
        self.config = config

    @abstractmethod
    def load_examples(self) -> list[NormalizedExample]:
        raise NotImplementedError

    def format_single_turn_prompt(
        self,
        example: NormalizedExample,
        *,
        system_prompt: str,
        final_answer_instruction: str,
    ) -> str:
        return build_single_turn_prompt(
            example,
            system_prompt=system_prompt,
            final_answer_instruction=final_answer_instruction,
        )

    def format_multiturn_prompt(
        self,
        example: NormalizedExample,
        history: list[HistoryTurn],
        *,
        system_prompt: str,
        final_answer_instruction: str,
        history_answer_prefix: str,
    ) -> str:
        return build_multi_turn_prompt(
            example,
            history,
            system_prompt=system_prompt,
            final_answer_instruction=final_answer_instruction,
            history_answer_prefix=history_answer_prefix,
        )

    def extract_final_answer(self, raw_output: str, example: NormalizedExample) -> ParseResult:
        benchmark_type = example.benchmark_type
        if benchmark_type in {"multiple_choice", "completion_choice"}:
            return parse_multiple_choice(raw_output, example.choices or [])
        if benchmark_type == "numeric_boxed":
            return parse_numeric_boxed(raw_output)
        if benchmark_type == "yes_no":
            return parse_yes_no(raw_output)
        if benchmark_type == "short_answer":
            return parse_short_answer(raw_output)
        return ParseResult(
            status="invalid",
            normalized_answer=None,
            parser_name="unsupported",
            reason_code=UNSUPPORTED_BENCHMARK_TYPE,
            raw_output=raw_output,
        )

    def score_prediction(self, example: NormalizedExample, raw_output: str) -> ScoreResult:
        parse = self.extract_final_answer(raw_output, example)
        normalized_gold = self.normalize_gold_answer(example)
        return ScoreResult(
            parse=parse,
            normalized_gold_answer=normalized_gold,
            is_correct=parse.status == "parsed" and normalized_gold is not None and parse.normalized_answer == normalized_gold,
            scoreable=normalized_gold is not None,
        )

    def normalize_gold_answer(self, example: NormalizedExample) -> str | None:
        if example.benchmark_type in {"multiple_choice", "completion_choice"}:
            return str(example.gold_answer).strip().upper()
        if example.benchmark_type == "numeric_boxed":
            return normalize_numeric_string(example.gold_answer)
        if example.benchmark_type == "yes_no":
            value = example.gold_answer.strip().lower()
            return value if value in {"yes", "no"} else None
        if example.benchmark_type == "short_answer":
            return normalize_short_text(example.gold_answer)
        return None

    def benchmark_domain(self) -> str:
        return self.domain

    def benchmark_type_name(self) -> str:
        return self.benchmark_type


class HFAdapter(BenchmarkAdapter):
    def _load_hf_split(self):
        kwargs = dict(self.config.extra_kwargs)
        if self.config.cache_dir:
            kwargs["cache_dir"] = self.config.cache_dir
        return load_dataset(
            path=self.config.path,
            name=self.config.subset,
            split=self.config.split,
            trust_remote_code=self.config.trust_remote_code,
            **kwargs,
        )

    def _load_local_jsonl(self):
        rows = []
        path = Path(self.config.local_path or "")
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    rows.append(json.loads(line))
        return rows

    def _apply_limit(self, items: list[NormalizedExample]) -> list[NormalizedExample]:
        if self.config.shuffle:
            import random

            rng = random.Random(self.config.seed)
            rng.shuffle(items)
        if self.config.limit is not None:
            return items[: self.config.limit]
        return items


def parse_multiple_choice(raw_output: str, choices: list[str]) -> ParseResult:
    if not raw_output.strip():
        return ParseResult("invalid", None, "mcq", EMPTY_OUTPUT, raw_output)
    answer_lines = [match.group(1).strip() for match in ANSWER_LINE_RE.finditer(raw_output)]
    if len(answer_lines) > 1:
        normalized = {candidate.strip().upper() for candidate in answer_lines}
        if len(normalized) > 1:
            return ParseResult("invalid", None, "mcq", CONFLICTING_FINAL_ANSWERS, raw_output)
    search_space = answer_lines[-1] if answer_lines else raw_output[-500:]
    match = LETTER_RE.search(search_space)
    if not match:
        return ParseResult("invalid", None, "mcq", PARSE_FAILURE, raw_output)
    answer = match.group(1).upper()
    if choices and (ord(answer) - ord("A") >= len(choices)):
        return ParseResult("invalid", None, "mcq", INVALID_OPTION_CHOICE, raw_output)
    return ParseResult("parsed", answer, "mcq", None, raw_output)


def parse_numeric_boxed(raw_output: str) -> ParseResult:
    if not raw_output.strip():
        return ParseResult("invalid", None, "numeric_boxed", EMPTY_OUTPUT, raw_output)
    boxed = BOXED_RE.findall(raw_output)
    if boxed:
        normalized = normalize_numeric_string(boxed[-1])
        if normalized is not None:
            return ParseResult("parsed", normalized, "numeric_boxed", None, raw_output)
    answer_lines = [match.group(1).strip() for match in ANSWER_LINE_RE.finditer(raw_output)]
    if answer_lines:
        normalized = normalize_numeric_string(answer_lines[-1])
        if normalized is not None:
            return ParseResult("parsed", normalized, "numeric_answer_line", None, raw_output)
    return ParseResult("invalid", None, "numeric_boxed", BOXED_MISSING, raw_output)


def parse_yes_no(raw_output: str) -> ParseResult:
    if not raw_output.strip():
        return ParseResult("invalid", None, "yes_no", EMPTY_OUTPUT, raw_output)
    matches = [match.group(1).lower() for match in YESNO_RE.finditer(raw_output)]
    matches = sorted(set(matches))
    if len(matches) == 1:
        return ParseResult("parsed", matches[0], "yes_no", None, raw_output)
    if len(matches) > 1:
        return ParseResult("invalid", None, "yes_no", CONFLICTING_FINAL_ANSWERS, raw_output)
    return ParseResult("invalid", None, "yes_no", PARSE_FAILURE, raw_output)


def parse_short_answer(raw_output: str) -> ParseResult:
    if not raw_output.strip():
        return ParseResult("invalid", None, "short_answer", EMPTY_OUTPUT, raw_output)
    answer_lines = [match.group(1).strip() for match in ANSWER_LINE_RE.finditer(raw_output)]
    if answer_lines:
        normalized = normalize_short_text(answer_lines[-1])
        return ParseResult("parsed", normalized, "short_answer", None, raw_output)
    lines = [line.strip() for line in raw_output.splitlines() if line.strip()]
    if not lines:
        return ParseResult("invalid", None, "short_answer", EMPTY_OUTPUT, raw_output)
    return ParseResult("parsed", normalize_short_text(lines[-1]), "short_answer_last_line", None, raw_output)


def normalize_numeric_string(value: str) -> str | None:
    candidate = value.strip().replace(",", "").replace("$", "").replace("%", "")
    candidate = candidate.removeprefix("####").strip().rstrip(".")
    if not candidate:
        return None
    try:
        if "/" in candidate and not any(ch.isalpha() for ch in candidate):
            fraction = Fraction(candidate)
            return _fraction_to_string(fraction)
        fraction = Fraction(Decimal(candidate))
        return _fraction_to_string(fraction)
    except (InvalidOperation, ValueError, ZeroDivisionError):
        matches = NUMERIC_RE.findall(candidate)
        for token in reversed(matches):
            try:
                if "/" in token:
                    return _fraction_to_string(Fraction(token))
                return _fraction_to_string(Fraction(Decimal(token)))
            except (InvalidOperation, ValueError, ZeroDivisionError):
                continue
    return None


def normalize_short_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().lower()


def _fraction_to_string(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
