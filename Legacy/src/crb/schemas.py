from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from typing import Any, Literal


AnswerType = Literal["mcq", "numeric", "freeform"]
EvaluationMode = Literal["multi_turn", "single_turn_flattened"]
HistoryMode = Literal["self_history", "oracle_history", "wrong_history"]
DummyType = Literal["same_domain", "cross_domain"]


@dataclass(slots=True)
class NormalizedItem:
    dataset_name: str
    split: str
    item_id: str
    domain: str | None
    subject: str | None
    question: str
    choices: list[str] | None
    answer: str
    answer_type: AnswerType
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class DataSourceConfig:
    dataset_name: str = ""
    adapter: str = ""
    path: str | None = None
    subset: str | None = None
    split: str = "test"
    local_path: str | None = None
    cache_dir: str | None = None
    limit: int | None = None
    shuffle: bool = False
    seed: int = 42
    trust_remote_code: bool = False
    extra_kwargs: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ModelConfig:
    engine: str = "vllm"
    model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"
    model_family: str = "generic"
    thinking_mode: str = "off"
    trust_remote_code: bool = True
    tensor_parallel_size: int | str = "auto"
    dtype: str = "auto"
    max_model_len: int | None = None
    gpu_memory_utilization: float = 0.9
    download_dir: str | None = None
    enforce_eager: bool = False
    swap_space: float = 4.0
    max_num_seqs: int | None = None
    seed: int = 42
    chat_template_kwargs: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class DecodingConfig:
    temperature: float = 0.0
    top_p: float = 1.0
    top_k: int = -1
    min_p: float = 0.0
    max_tokens: int = 256
    repetition_penalty: float = 1.0
    presence_penalty: float = 0.0
    stop: list[str] = field(default_factory=list)
    target_structured_choice: list[str] = field(default_factory=list)
    target_structured_regex: str | None = None
    target_choice_from_item_choices: bool = False


@dataclass(slots=True)
class PromptConfig:
    system_prompt: str = (
        "You are a precise evaluation assistant. Solve the user's problem carefully, but the "
        "final line must be exactly `Answer: <final_answer>` using a single canonical answer."
    )
    final_answer_instruction: str = (
        "Reply with reasoning if needed, but end with exactly one final line in the form "
        "`Answer: <final_answer>`."
    )
    history_answer_prefix: str = "Answer:"
    use_canonical_history: bool = True
    target_thinking_mode: Literal["default", "think", "no_think"] = "default"
    target_response_prefill: str | None = None


@dataclass(slots=True)
class RuntimeConfig:
    output_root: str = "results"
    log_dir: str = "logs"
    manifest_dir: str = "results/manifests"
    summary_csv: str = "results/summary/scoreboard.csv"
    resume: bool = True
    skip_completed: bool = True
    save_partial_every: int = 1
    timeout_seconds: int | None = None
    num_workers: int = 1


@dataclass(slots=True)
class ExperimentConfig:
    name: str
    seed: int
    num_samples: int | None = None
    tags: list[str] = field(default_factory=list)


@dataclass(slots=True)
class EvaluationConfig:
    evaluation_mode: EvaluationMode = "multi_turn"
    history_mode: HistoryMode = "oracle_history"
    dummy_type: DummyType = "same_domain"
    k: int = 0
    manifest_k_values: list[int] = field(default_factory=lambda: [0, 2, 4, 8])
    target: DataSourceConfig = field(default_factory=DataSourceConfig)
    dummy_sources: list[DataSourceConfig] = field(default_factory=list)


@dataclass(slots=True)
class RunConfig:
    experiment: ExperimentConfig
    model: ModelConfig
    decoding: DecodingConfig
    prompt: PromptConfig
    runtime: RuntimeConfig
    evaluation: EvaluationConfig

    def to_dict(self) -> dict[str, Any]:
        return dataclass_to_dict(self)


@dataclass(slots=True)
class ParsedAnswer:
    raw_output: str
    normalized_answer: str | None
    parser_name: str
    status: Literal["parsed", "invalid"]
    error_type: str | None = None


@dataclass(slots=True)
class ScoreResult:
    parsed: ParsedAnswer
    gold_answer: str
    normalized_gold_answer: str
    is_correct: bool


@dataclass(slots=True)
class HistoryTurn:
    item_id: str
    question: str
    choices: list[str] | None
    normalized_answer: str | None
    raw_output: str | None
    answer_source: Literal["oracle", "self", "wrong"]
    parse_status: str
    error_type: str | None = None
    dataset_name: str | None = None
    subject: str | None = None
    domain: str | None = None


@dataclass(slots=True)
class ManifestEntry:
    target_item_id: str
    target_dataset_name: str
    target_subject: str | None
    target_domain: str | None
    dummy_ids_by_type: dict[str, list[str]]


@dataclass(slots=True)
class EvaluationManifest:
    manifest_id: str
    config_hash: str
    seed: int
    ks: list[int]
    target_sources: list[dict[str, Any]]
    dummy_sources: list[dict[str, Any]]
    entries: list[ManifestEntry]

    def to_dict(self) -> dict[str, Any]:
        return dataclass_to_dict(self)


def dataclass_to_dict(value: Any) -> Any:
    if is_dataclass(value):
        return {key: dataclass_to_dict(val) for key, val in asdict(value).items()}
    if isinstance(value, list):
        return [dataclass_to_dict(item) for item in value]
    if isinstance(value, dict):
        return {key: dataclass_to_dict(val) for key, val in value.items()}
    return value
