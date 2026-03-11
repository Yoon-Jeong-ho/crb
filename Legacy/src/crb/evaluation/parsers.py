from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from fractions import Fraction

from crb.schemas import NormalizedItem, ParsedAnswer


MCQ_STRICT_RE = re.compile(r"^Answer\s*:\s*([A-J])\s*$", re.IGNORECASE)
MCQ_FALLBACK_RE = re.compile(r"^\s*\(?([A-J])[\)\.\:]?(?:\s|$)", re.IGNORECASE)
ANSWER_LINE_RE = re.compile(r"Answer\s*:\s*(.+)", re.IGNORECASE)
MCQ_REASONING_PATTERNS = [
    re.compile(r"\b(?:answer|option|choice)\s*(?:is|:)\s*([A-J])\b", re.IGNORECASE),
    re.compile(r"\bwhich is\s*([A-J])\b", re.IGNORECASE),
    re.compile(r"\btherefore\s*,?\s*(?:the\s+)?(?:answer|option|choice)\s*(?:is|:)\s*([A-J])\b", re.IGNORECASE),
    re.compile(r"\bso\s*,?\s*(?:the\s+)?(?:answer|option|choice)\s*(?:is|:)\s*([A-J])\b", re.IGNORECASE),
]
BOXED_RE = re.compile(r"\\boxed\{([^{}]+)\}")
NUMERIC_TOKEN_RE = re.compile(r"[-+]?\d+(?:\.\d+)?(?:/\d+)?")



def parse_answer(item: NormalizedItem, raw_output: str) -> ParsedAnswer:
    if item.answer_type == "mcq":
        return parse_mcq_answer(raw_output)
    if item.answer_type == "numeric":
        return parse_numeric_answer(raw_output)
    return parse_freeform_answer(raw_output)



def parse_mcq_answer(raw_output: str) -> ParsedAnswer:
    lines = [line.strip() for line in raw_output.splitlines() if line.strip()]
    for line in reversed(lines):
        match = MCQ_STRICT_RE.match(line)
        if match:
            return ParsedAnswer(
                raw_output=raw_output,
                normalized_answer=match.group(1).upper(),
                parser_name="mcq_strict",
                status="parsed",
            )

    reasoning_tail = raw_output[-1600:]
    reasoning_candidates: list[str] = []
    for pattern in MCQ_REASONING_PATTERNS:
        reasoning_candidates.extend(match.group(1).upper() for match in pattern.finditer(reasoning_tail))
    if reasoning_candidates:
        return ParsedAnswer(
            raw_output=raw_output,
            normalized_answer=reasoning_candidates[-1],
            parser_name="mcq_reasoning_fallback",
            status="parsed",
        )

    candidates: list[str] = []
    for line in lines[-20:]:
        if "answer" in line.lower():
            answer_match = ANSWER_LINE_RE.search(line)
            if answer_match:
                letter_match = MCQ_FALLBACK_RE.search(answer_match.group(1).strip())
                if letter_match:
                    candidates.append(letter_match.group(1).upper())
                    continue
        line_match = MCQ_FALLBACK_RE.search(line)
        if line_match:
            candidates.append(line_match.group(1).upper())
    candidates = sorted(set(candidates))
    if len(candidates) == 1:
        return ParsedAnswer(
            raw_output=raw_output,
            normalized_answer=candidates[0],
            parser_name="mcq_fallback",
            status="parsed",
        )
    error = "ambiguous_mcq_answer" if len(candidates) > 1 else "parse_failure"
    return ParsedAnswer(
        raw_output=raw_output,
        normalized_answer=None,
        parser_name="mcq_fallback",
        status="invalid",
        error_type=error,
    )



def parse_numeric_answer(raw_output: str) -> ParsedAnswer:
    lines = [line.strip() for line in raw_output.splitlines() if line.strip()]
    for line in reversed(lines):
        match = MCQ_STRICT_RE.match(line)
        if match:
            return ParsedAnswer(
                raw_output=raw_output,
                normalized_answer=match.group(1).upper(),
                parser_name="numeric_but_letter",
                status="invalid",
                error_type="letter_output_for_numeric",
            )
        match = ANSWER_LINE_RE.search(line)
        if match:
            normalized = _normalize_numeric_fragment(match.group(1))
            if normalized is not None:
                return ParsedAnswer(
                    raw_output=raw_output,
                    normalized_answer=normalized,
                    parser_name="numeric_strict",
                    status="parsed",
                )
    answer_spans = [match.group(1) for match in ANSWER_LINE_RE.finditer(raw_output)]
    normalized_spans = [
        normalized
        for span in answer_spans
        if (normalized := _normalize_numeric_fragment(span)) is not None
    ]
    if normalized_spans:
        return ParsedAnswer(
            raw_output=raw_output,
            normalized_answer=normalized_spans[-1],
            parser_name="numeric_answer_span_fallback",
            status="parsed",
        )
    numbers: list[str] = []
    for line in lines[-4:]:
        normalized = _normalize_numeric_fragment(line)
        if normalized is not None:
            numbers.append(normalized)
    numbers = sorted(set(numbers))
    if len(numbers) == 1:
        return ParsedAnswer(
            raw_output=raw_output,
            normalized_answer=numbers[0],
            parser_name="numeric_fallback",
            status="parsed",
        )
    return ParsedAnswer(
        raw_output=raw_output,
        normalized_answer=None,
        parser_name="numeric_fallback",
        status="invalid",
        error_type="parse_failure" if not numbers else "ambiguous_numeric_answer",
    )



def parse_freeform_answer(raw_output: str) -> ParsedAnswer:
    lines = [line.strip() for line in raw_output.splitlines() if line.strip()]
    if not lines:
        return ParsedAnswer(
            raw_output=raw_output,
            normalized_answer=None,
            parser_name="freeform",
            status="invalid",
            error_type="empty_output",
        )
    for line in reversed(lines):
        match = ANSWER_LINE_RE.search(line)
        if match:
            return ParsedAnswer(
                raw_output=raw_output,
                normalized_answer=match.group(1).strip(),
                parser_name="freeform",
                status="parsed",
            )
    return ParsedAnswer(
        raw_output=raw_output,
        normalized_answer=lines[-1],
        parser_name="freeform_last_line",
        status="parsed",
    )



def normalize_numeric_string(value: str) -> str | None:
    candidate = value.strip()
    if not candidate:
        return None
    boxed = BOXED_RE.search(candidate)
    if boxed:
        candidate = boxed.group(1).strip()
    candidate = candidate.replace(",", "")
    candidate = candidate.replace("$", "")
    candidate = candidate.replace("%", "")
    candidate = candidate.strip().rstrip(".")
    candidate = candidate.removeprefix("=").strip()
    if candidate.startswith("####"):
        candidate = candidate.removeprefix("####").strip()
    if not candidate:
        return None
    try:
        if "/" in candidate and not any(ch.isalpha() for ch in candidate):
            fraction = Fraction(candidate)
            return _fraction_to_string(fraction)
        decimal = Decimal(candidate)
        fraction = Fraction(decimal)
        return _fraction_to_string(fraction)
    except (InvalidOperation, ValueError, ZeroDivisionError):
        return None


def _normalize_numeric_fragment(value: str) -> str | None:
    normalized = normalize_numeric_string(value)
    if normalized is not None:
        return normalized
    matches = NUMERIC_TOKEN_RE.findall(value)
    if not matches:
        return None
    for token in reversed(matches):
        normalized = normalize_numeric_string(token)
        if normalized is not None:
            return normalized
    return None



def _fraction_to_string(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"
