from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from crb.schemas import DataSourceConfig, NormalizedItem

LoaderFn = Callable[[DataSourceConfig], list[NormalizedItem]]


class DatasetRegistry:
    def __init__(self) -> None:
        self._loaders: dict[str, LoaderFn] = {}

    def register(self, name: str, loader: LoaderFn) -> None:
        self._loaders[name] = loader

    def get(self, name: str) -> LoaderFn:
        if name not in self._loaders:
            raise KeyError(f"Unknown dataset adapter: {name}")
        return self._loaders[name]


registry = DatasetRegistry()


LETTER_CHOICES = list("ABCDEFGHIJ")


KEY_ALIASES = {
    "question": ["question", "prompt", "problem", "query", "Question", "Problem"],
    "subject": ["subject", "category", "subdomain", "discipline", "Subdomain"],
    "domain": ["domain", "high_level_domain", "field", "High-level domain"],
    "answer": ["answer", "target", "correct_answer", "label", "answer_key", "Answer"],
    "choices": ["choices", "options", "candidates"],
    "item_id": ["item_id", "id", "question_id", "uid", "Record ID", "ID"],
}


def _first_present(example: dict[str, Any], keys: list[str], default: Any = None) -> Any:
    for key in keys:
        if key in example and example[key] not in (None, ""):
            return example[key]
    return default


def _normalize_choice_answer(answer: Any, *, choices: list[str] | None = None) -> str:
    if isinstance(answer, int):
        return LETTER_CHOICES[answer]
    if isinstance(answer, str):
        cleaned = answer.strip()
        if cleaned.isdigit() and choices is not None:
            return LETTER_CHOICES[int(cleaned)]
        if len(cleaned) == 1 and cleaned.upper() in LETTER_CHOICES:
            return cleaned.upper()
        return cleaned
    raise ValueError(f"Unsupported choice answer: {answer!r}")


def canonicalize_subject(value: Any) -> str | None:
    if value is None:
        return None
    cleaned = str(value).strip()
    return cleaned or None


def canonicalize_domain(*, dataset_name: str, raw_domain: Any, raw_subject: Any) -> str | None:
    candidate = str(raw_domain or raw_subject or dataset_name).strip().lower()
    if not candidate:
        return None

    keyword_groups = {
        "math": ["math", "algebra", "geometry", "calculus", "statistics", "arithmetic", "number", "aime"],
        "physics": ["physics", "quantum", "mechanics", "electricity", "thermo"],
        "chemistry": ["chemistry", "chemical"],
        "biology": ["biology", "genetics", "anatomy", "ecology", "microbiology"],
        "computer_science": ["computer", "programming", "machine_learning", "machine learning"],
        "economics": ["economics", "economy", "finance", "accounting"],
        "law": ["law", "jurisprudence"],
        "history": ["history"],
        "philosophy": ["philosophy", "ethics", "logic"],
        "psychology": ["psychology"],
        "medicine": ["medicine", "clinical", "medical", "health"],
        "humanities": ["humanities", "literature", "linguistics", "language"],
    }
    for normalized, keywords in keyword_groups.items():
        if any(keyword in candidate for keyword in keywords):
            return normalized
    return candidate.replace(" ", "_")


def _normalize_item_id(example: dict[str, Any], dataset_name: str, split: str, idx: int) -> str:
    explicit = _first_present(example, KEY_ALIASES["item_id"])
    if explicit is None:
        return f"{dataset_name}:{split}:{idx}"
    return f"{dataset_name}:{split}:{explicit}"


def _normalize_mcq_record(example: dict[str, Any], *, dataset_name: str, split: str, idx: int) -> NormalizedItem:
    question = str(_first_present(example, KEY_ALIASES["question"]))
    raw_choices = _first_present(example, KEY_ALIASES["choices"])
    if isinstance(raw_choices, dict):
        raw_choices = list(raw_choices.values())
    elif raw_choices is None:
        options = [example[key] for key in LETTER_CHOICES[:4] if key in example]
        raw_choices = options if options else None
    choices = [str(choice).strip() for choice in raw_choices] if raw_choices else None
    answer = _normalize_choice_answer(_first_present(example, KEY_ALIASES["answer"]), choices=choices)
    subject = canonicalize_subject(_first_present(example, KEY_ALIASES["subject"]))
    domain = canonicalize_domain(
        dataset_name=dataset_name,
        raw_domain=_first_present(example, KEY_ALIASES["domain"], default=subject),
        raw_subject=subject,
    )
    return NormalizedItem(
        dataset_name=dataset_name,
        split=split,
        item_id=_normalize_item_id(example, dataset_name, split, idx),
        domain=domain,
        subject=subject,
        question=question,
        choices=choices,
        answer=answer,
        answer_type="mcq",
        metadata={"source_record": example},
    )


def _normalize_numeric_record(example: dict[str, Any], *, dataset_name: str, split: str, idx: int) -> NormalizedItem:
    question = str(_first_present(example, KEY_ALIASES["question"]))
    answer = _first_present(example, KEY_ALIASES["answer"])
    subject = canonicalize_subject(_first_present(example, KEY_ALIASES["subject"], default=dataset_name))
    domain = canonicalize_domain(
        dataset_name=dataset_name,
        raw_domain=_first_present(example, KEY_ALIASES["domain"], default=subject),
        raw_subject=subject,
    )
    return NormalizedItem(
        dataset_name=dataset_name,
        split=split,
        item_id=_normalize_item_id(example, dataset_name, split, idx),
        domain=domain,
        subject=subject,
        question=question,
        choices=None,
        answer=str(answer).strip(),
        answer_type="numeric",
        metadata={"source_record": example},
    )


def jsonl_loader(config: DataSourceConfig) -> list[NormalizedItem]:
    if not config.local_path:
        raise ValueError("jsonl adapter requires local_path")
    path = Path(config.local_path)
    items: list[NormalizedItem] = []
    with path.open("r", encoding="utf-8") as handle:
        for idx, line in enumerate(handle):
            record = json.loads(line)
            answer_type = record.get("answer_type", "mcq")
            if answer_type == "mcq":
                item = _normalize_mcq_record(record, dataset_name=config.dataset_name, split=config.split, idx=idx)
            elif answer_type == "numeric":
                item = _normalize_numeric_record(record, dataset_name=config.dataset_name, split=config.split, idx=idx)
            else:
                raise ValueError(f"Unsupported answer_type in jsonl fixture: {answer_type}")
            items.append(item)
    return items


registry.register("jsonl", jsonl_loader)


def _resolve_single_turn_pool_path(config: DataSourceConfig) -> Path:
    if config.local_path:
        return Path(config.local_path)
    raw_pool_thinking_mode = config.pool_thinking_mode
    pool_thinking_mode = raw_pool_thinking_mode
    if isinstance(pool_thinking_mode, bool):
        pool_thinking_mode = "on" if pool_thinking_mode else "off"
    missing = [
        field_name
        for field_name, value in (
            ("pool_model_slug", config.pool_model_slug),
            ("pool_thinking_mode", pool_thinking_mode),
            ("pool_label", config.pool_label),
        )
        if not value
    ]
    if missing:
        raise ValueError(
            f"single_turn_pool adapter requires {', '.join(missing)} when local_path is not set"
        )
    root = Path(config.pool_root or "results/pools/single_turn")
    preferred = root / str(config.pool_model_slug) / f"thinking_{pool_thinking_mode}" / config.dataset_name / config.split / f"{config.pool_label}.jsonl"
    if preferred.exists():
        return preferred
    if raw_pool_thinking_mode is not None:
        legacy = root / str(config.pool_model_slug) / f"thinking_{raw_pool_thinking_mode}" / config.dataset_name / config.split / f"{config.pool_label}.jsonl"
        if legacy.exists():
            return legacy
    if isinstance(pool_thinking_mode, str) and pool_thinking_mode in {"off", "on"}:
        legacy_bool = "False" if pool_thinking_mode == "off" else "True"
        legacy = root / str(config.pool_model_slug) / f"thinking_{legacy_bool}" / config.dataset_name / config.split / f"{config.pool_label}.jsonl"
        if legacy.exists():
            return legacy
    return preferred


def single_turn_pool_loader(config: DataSourceConfig) -> list[NormalizedItem]:
    path = _resolve_single_turn_pool_path(config)
    items: list[NormalizedItem] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            choices = record.get("choices")
            items.append(
                NormalizedItem(
                    dataset_name=str(record.get("dataset_name") or config.dataset_name),
                    split=str(record.get("split") or config.split),
                    item_id=str(record["item_id"]),
                    domain=record.get("domain"),
                    subject=record.get("subject"),
                    question=str(record["question"]),
                    choices=choices if isinstance(choices, list) else None,
                    answer=str(record["answer"]),
                    answer_type=str(record.get("answer_type") or ("mcq" if choices else "numeric")),  # type: ignore[arg-type]
                    metadata={
                        "source_record": record,
                        "pool_model_slug": config.pool_model_slug,
                        "pool_thinking_mode": config.pool_thinking_mode,
                        "pool_label": config.pool_label,
                    },
                )
            )
    return items


registry.register("single_turn_pool", single_turn_pool_loader)


def load_items(config: DataSourceConfig) -> list[NormalizedItem]:
    return registry.get(config.adapter)(config)
