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
    "question": ["question", "prompt", "problem", "query"],
    "subject": ["subject", "category", "subdomain", "discipline"],
    "domain": ["domain", "high_level_domain", "field"],
    "answer": ["answer", "target", "correct_answer", "label", "answer_key"],
    "choices": ["choices", "options", "candidates"],
    "item_id": ["item_id", "id", "question_id", "uid"],
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
    subject = _first_present(example, KEY_ALIASES["subject"])
    domain = _first_present(example, KEY_ALIASES["domain"], default=subject)
    return NormalizedItem(
        dataset_name=dataset_name,
        split=split,
        item_id=_normalize_item_id(example, dataset_name, split, idx),
        domain=str(domain) if domain is not None else None,
        subject=str(subject) if subject is not None else None,
        question=question,
        choices=choices,
        answer=answer,
        answer_type="mcq",
        metadata={"source_record": example},
    )



def _normalize_numeric_record(example: dict[str, Any], *, dataset_name: str, split: str, idx: int) -> NormalizedItem:
    question = str(_first_present(example, KEY_ALIASES["question"]))
    answer = _first_present(example, KEY_ALIASES["answer"])
    subject = _first_present(example, KEY_ALIASES["subject"], default=dataset_name)
    domain = _first_present(example, KEY_ALIASES["domain"], default=subject)
    return NormalizedItem(
        dataset_name=dataset_name,
        split=split,
        item_id=_normalize_item_id(example, dataset_name, split, idx),
        domain=str(domain) if domain is not None else None,
        subject=str(subject) if subject is not None else None,
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


def load_items(config: DataSourceConfig) -> list[NormalizedItem]:
    return registry.get(config.adapter)(config)
