from __future__ import annotations

from dataclasses import dataclass

from crb_v2.failures import CONTEXT_OVERFLOW, SKIPPED_DUE_TO_BUDGET, TRUNCATION_APPLIED
from crb_v2.prompts import build_multi_turn_prompt
from crb_v2.types import HistoryTurn, NormalizedExample


@dataclass(slots=True)
class BudgetResult:
    prompt_text: str | None
    prompt_token_count: int | None
    effective_history: list[HistoryTurn]
    reason_codes: list[str]



def fit_history_to_budget(
    *,
    example: NormalizedExample,
    history: list[HistoryTurn],
    engine,
    max_context_tokens: int,
    max_new_tokens: int,
    system_prompt: str,
    final_answer_instruction: str,
    history_answer_prefix: str,
    compaction_policy: str,
) -> BudgetResult:
    if compaction_policy != "drop_oldest_history":
        raise ValueError(f"Unsupported compaction policy: {compaction_policy}")
    working = list(history)
    reason_codes: list[str] = []
    while True:
        prompt_text = build_multi_turn_prompt(
            example,
            working,
            system_prompt=system_prompt,
            final_answer_instruction=final_answer_instruction,
            history_answer_prefix=history_answer_prefix,
        )
        prompt_tokens = engine.count_tokens(prompt_text)
        if prompt_tokens + max_new_tokens <= max_context_tokens:
            return BudgetResult(prompt_text, prompt_tokens, working, reason_codes)
        if not working:
            return BudgetResult(None, prompt_tokens, [], [CONTEXT_OVERFLOW, SKIPPED_DUE_TO_BUDGET])
        working = working[1:]
        if TRUNCATION_APPLIED not in reason_codes:
            reason_codes.append(TRUNCATION_APPLIED)
