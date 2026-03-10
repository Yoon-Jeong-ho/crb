from __future__ import annotations

import re
from typing import Any

from datasets import load_dataset

from crb.datasets.base import (
    KEY_ALIASES,
    _first_present,
    _normalize_choice_answer,
    _normalize_item_id,
    registry,
)
from crb.schemas import DataSourceConfig, NormalizedItem


LETTER_CHOICES = list("ABCDEFGHIJ")
GSM8K_ANSWER_RE = re.compile(r"####\s*([^\n]+)")



def _load_hf_split(config: DataSourceConfig):
    kwargs = dict(config.extra_kwargs)
    if config.cache_dir:
        kwargs["cache_dir"] = config.cache_dir
    if config.path is None:
        raise ValueError(f"Dataset adapter `{config.adapter}` requires `path`")
    return load_dataset(
        path=config.path,
        name=config.subset,
        split=config.split,
        trust_remote_code=config.trust_remote_code,
        **kwargs,
    )



def mmlu_loader(config: DataSourceConfig) -> list[NormalizedItem]:
    dataset = _load_hf_split(config)
    items: list[NormalizedItem] = []
    for idx, example in enumerate(dataset):
        question = str(_first_present(example, KEY_ALIASES["question"]))
        choices = example.get("choices") or example.get("options") or example.get("answers")
        if isinstance(choices, dict):
            choices = list(choices.values())
        choices = [str(choice).strip() for choice in choices]
        answer = _normalize_choice_answer(_first_present(example, KEY_ALIASES["answer"]), choices=choices)
        subject = _first_present(example, KEY_ALIASES["subject"], default=config.subset)
        domain = _first_present(example, KEY_ALIASES["domain"], default=subject)
        items.append(
            NormalizedItem(
                dataset_name=config.dataset_name,
                split=config.split,
                item_id=_normalize_item_id(example, config.dataset_name, config.split, idx),
                domain=str(domain) if domain is not None else None,
                subject=str(subject) if subject is not None else None,
                question=question,
                choices=choices,
                answer=answer,
                answer_type="mcq",
                metadata={"source_record": dict(example)},
            )
        )
    return items



def gsm8k_loader(config: DataSourceConfig) -> list[NormalizedItem]:
    dataset = _load_hf_split(config)
    items: list[NormalizedItem] = []
    for idx, example in enumerate(dataset):
        raw_answer = str(example.get("answer", "")).strip()
        match = GSM8K_ANSWER_RE.search(raw_answer)
        normalized_answer = match.group(1).strip() if match else raw_answer
        items.append(
            NormalizedItem(
                dataset_name=config.dataset_name,
                split=config.split,
                item_id=_normalize_item_id(example, config.dataset_name, config.split, idx),
                domain="math",
                subject="arithmetic",
                question=str(example["question"]).strip(),
                choices=None,
                answer=normalized_answer,
                answer_type="numeric",
                metadata={"source_record": dict(example), "solution": raw_answer},
            )
        )
    return items



def gpqa_loader(config: DataSourceConfig) -> list[NormalizedItem]:
    dataset = _load_hf_split(config)
    items: list[NormalizedItem] = []
    for idx, example in enumerate(dataset):
        question = str(
            example.get("Question")
            or example.get("question")
            or example.get("prompt")
        ).strip()
        correct = str(example.get("Correct Answer") or example.get("correct_answer") or example.get("answer"))
        distractors = [
            str(value)
            for key, value in example.items()
            if str(key).lower().startswith("incorrect answer") or str(key).lower().startswith("distractor")
        ]
        if not distractors:
            distractors = [
                str(example[key])
                for key in ["Incorrect Answer 1", "Incorrect Answer 2", "Incorrect Answer 3"]
                if key in example
            ]
        choices = [correct, *distractors]
        answer_letter = LETTER_CHOICES[0]
        subject = example.get("Subdomain") or example.get("subdomain") or "gpqa"
        domain = example.get("High-level domain") or example.get("high_level_domain") or subject
        items.append(
            NormalizedItem(
                dataset_name=config.dataset_name,
                split=config.split,
                item_id=_normalize_item_id(example, config.dataset_name, config.split, idx),
                domain=str(domain),
                subject=str(subject),
                question=question,
                choices=choices,
                answer=answer_letter,
                answer_type="mcq",
                metadata={"source_record": dict(example), "correct_choice_text": correct},
            )
        )
    return items


registry.register("mmlu", mmlu_loader)
registry.register("gsm8k", gsm8k_loader)
registry.register("gpqa", gpqa_loader)
