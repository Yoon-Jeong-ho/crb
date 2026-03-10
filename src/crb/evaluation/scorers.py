from __future__ import annotations

from crb.evaluation.parsers import normalize_numeric_string, parse_answer
from crb.schemas import NormalizedItem, ScoreResult



def score_output(item: NormalizedItem, raw_output: str) -> ScoreResult:
    parsed = parse_answer(item, raw_output)
    normalized_gold = normalize_gold_answer(item)
    is_correct = parsed.status == "parsed" and parsed.normalized_answer == normalized_gold
    return ScoreResult(
        parsed=parsed,
        gold_answer=item.answer,
        normalized_gold_answer=normalized_gold,
        is_correct=is_correct,
    )



def normalize_gold_answer(item: NormalizedItem) -> str:
    if item.answer_type == "mcq":
        return item.answer.strip().upper()
    if item.answer_type == "numeric":
        normalized = normalize_numeric_string(item.answer)
        if normalized is None:
            raise ValueError(f"Could not normalize numeric gold answer for {item.item_id}: {item.answer}")
        return normalized
    return item.answer.strip()
