from __future__ import annotations

from dataclasses import dataclass

PARSE_FAILURE = "parse_failure"
FORMAT_FAILURE = "format_failure"
BOXED_MISSING = "boxed_missing"
INVALID_OPTION_CHOICE = "invalid_option_choice"
EMPTY_OUTPUT = "empty_output"
CONFLICTING_FINAL_ANSWERS = "conflicting_final_answers"
CONTEXT_OVERFLOW = "context_overflow"
TRUNCATION_APPLIED = "truncation_applied"
SKIPPED_DUE_TO_BUDGET = "skipped_due_to_budget"
INVALID_GENERATION = "invalid_generation"
UNSUPPORTED_BENCHMARK_TYPE = "unsupported_benchmark_type"
RUNTIME_EXCEPTION = "runtime_exception"
INSUFFICIENT_DUMMY_POOL = "insufficient_dummy_pool"
RUNTIME_TIMEOUT = "runtime_timeout"

PARSE_RELATED = {PARSE_FAILURE, BOXED_MISSING, INVALID_OPTION_CHOICE, EMPTY_OUTPUT, CONFLICTING_FINAL_ANSWERS}
FORMAT_RELATED = {FORMAT_FAILURE, BOXED_MISSING, INVALID_OPTION_CHOICE, EMPTY_OUTPUT, CONFLICTING_FINAL_ANSWERS, INVALID_GENERATION}
SKIP_RELATED = {CONTEXT_OVERFLOW, SKIPPED_DUE_TO_BUDGET, INSUFFICIENT_DUMMY_POOL}


@dataclass(frozen=True, slots=True)
class FailureSummary:
    parse_failure: bool
    format_failure: bool
    skipped: bool



def summarize_reason_codes(reason_codes: list[str]) -> FailureSummary:
    reason_set = set(reason_codes)
    return FailureSummary(
        parse_failure=bool(reason_set & PARSE_RELATED),
        format_failure=bool(reason_set & FORMAT_RELATED),
        skipped=bool(reason_set & SKIP_RELATED),
    )



def eligible_for_incorrect_pool(parse_status: str, scoreable: bool, is_correct: bool, reason_codes: list[str]) -> bool:
    return parse_status == "parsed" and scoreable and not is_correct and not bool(set(reason_codes) & FORMAT_RELATED)



def eligible_for_correct_pool(parse_status: str, scoreable: bool, is_correct: bool, reason_codes: list[str]) -> bool:
    return parse_status == "parsed" and scoreable and is_correct and not bool(set(reason_codes) & FORMAT_RELATED)
