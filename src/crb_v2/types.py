from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from typing import Any, Literal

BenchmarkType = Literal[
    "multiple_choice",
    "numeric_boxed",
    "short_answer",
    "yes_no",
    "completion_choice",
]
RelationType = Literal["same_benchmark", "same_domain_other_benchmark", "cross_domain"]
ProvenanceType = Literal["model_correct", "model_incorrect", "oracle"]
PromptStyle = Literal["flat"]


@dataclass(slots=True)
class NormalizedExample:
    benchmark_name: str
    split: str
    example_id: str
    domain: str
    subdomain: str | None
    question: str
    choices: list[str] | None
    gold_answer: str
    benchmark_type: BenchmarkType
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ParseResult:
    status: Literal["parsed", "invalid"]
    normalized_answer: str | None
    parser_name: str
    reason_code: str | None
    raw_output: str


@dataclass(slots=True)
class ScoreResult:
    parse: ParseResult
    normalized_gold_answer: str | None
    is_correct: bool
    scoreable: bool


@dataclass(slots=True)
class HistoryTurn:
    source_example_id: str
    benchmark_name: str
    question: str
    choices: list[str] | None
    answer: str | None
    provenance: ProvenanceType
    source_domain: str
    source_subdomain: str | None


@dataclass(slots=True)
class PoolRecord:
    benchmark_name: str
    split: str
    example_id: str
    domain: str
    subdomain: str | None
    question: str
    choices: list[str] | None
    answer: str
    provenance: ProvenanceType
    source_model_key: str | None
    source_benchmark_name: str
    source_result_path: str | None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ManifestEntry:
    target_example_id: str
    relation: RelationType
    provenance: ProvenanceType
    ordered_dummy_ids: list[str]
    ordered_dummy_benchmarks: list[str]


@dataclass(slots=True)
class RunItemRecord:
    model_key: str
    benchmark_name: str
    split: str
    example_id: str
    stage: Literal["baseline", "sweep"]
    relation: str
    provenance: str
    requested_k: int
    effective_k: int
    seed: int
    prompt_style: str
    prompt_token_count: int | None
    completion_token_count: int | None
    reason_codes: list[str]
    raw_output: str
    parsed_answer: str | None
    parse_status: str
    parser_name: str | None
    normalized_gold_answer: str | None
    scoreable: bool
    is_correct: bool
    prompt_text_path: str | None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AggregateRow:
    model_key: str
    benchmark_name: str
    stage: str
    relation: str
    provenance: str
    k: int
    num_items: int
    valid_answer_rate: float
    accuracy: float
    parse_failure_rate: float
    format_failure_rate: float
    skipped_rate: float
    delta_vs_k0: float | None



def to_dict(value: Any) -> Any:
    if is_dataclass(value):
        return {key: to_dict(val) for key, val in asdict(value).items()}
    if isinstance(value, list):
        return [to_dict(item) for item in value]
    if isinstance(value, dict):
        return {key: to_dict(val) for key, val in value.items()}
    return value
