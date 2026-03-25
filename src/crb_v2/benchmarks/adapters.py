from __future__ import annotations

from typing import Any

from crb_v2.benchmarks.base import HFAdapter
from crb_v2.types import NormalizedExample


class GSM8KAdapter(HFAdapter):
    benchmark_name = "gsm8k"
    domain = "math"
    benchmark_type = "numeric_boxed"

    def load_examples(self) -> list[NormalizedExample]:
        dataset = self._load_hf_split() if not self.config.local_path else self._load_local_jsonl()
        items: list[NormalizedExample] = []
        for idx, row in enumerate(dataset):
            items.append(NormalizedExample(self.benchmark_name, self.config.split or "test", f"gsm8k:{idx}", self.domain, "arithmetic", str(row.get("question") or row.get("problem") or row.get("prompt")).strip(), None, str(row.get("answer") or row.get("final_answer") or row.get("target")).strip(), self.benchmark_type, {"source_record": dict(row)}))
        return self._apply_limit(items)


class MATH500Adapter(HFAdapter):
    benchmark_name = "math500"
    domain = "math"
    benchmark_type = "numeric_boxed"

    def load_examples(self) -> list[NormalizedExample]:
        dataset = self._load_hf_split() if not self.config.local_path else self._load_local_jsonl()
        items: list[NormalizedExample] = []
        for idx, row in enumerate(dataset):
            items.append(NormalizedExample(self.benchmark_name, self.config.split or "test", f"math500:{idx}", self.domain, str(row.get("subject") or row.get("category") or "math500").strip().lower(), str(row.get("problem") or row.get("question") or row.get("prompt")).strip(), None, str(row.get("answer") or row.get("final_answer") or row.get("solution") or row.get("target")).strip(), self.benchmark_type, {"source_record": dict(row)}))
        return self._apply_limit(items)


class GPQAAdapter(HFAdapter):
    benchmark_name = "gpqa"
    domain = "science"
    benchmark_type = "multiple_choice"

    def load_examples(self) -> list[NormalizedExample]:
        import random
        from crb_v2.utils import stable_hash

        dataset = self._load_hf_split() if not self.config.local_path else self._load_local_jsonl()
        items: list[NormalizedExample] = []
        for idx, row in enumerate(dataset):
            question = str(row.get("Question") or row.get("question") or row.get("prompt")).strip()
            correct = str(row.get("Correct Answer") or row.get("correct_answer") or row.get("answer")).strip()
            distractors = [
                str(value).strip()
                for key, value in row.items()
                if str(key).lower().startswith("incorrect answer") or str(key).lower().startswith("distractor")
            ]
            if not distractors:
                distractors = [str(row[key]).strip() for key in ["Incorrect Answer 1", "Incorrect Answer 2", "Incorrect Answer 3"] if key in row]
            choices = [correct, *distractors]
            item_id = f"gpqa:{idx}"
            order = list(range(len(choices)))
            rng = random.Random(int(stable_hash({"item_id": item_id, "seed": self.config.seed}, length=16), 16))
            rng.shuffle(order)
            shuffled = [choices[position] for position in order]
            answer = chr(ord("A") + order.index(0))
            items.append(NormalizedExample(self.benchmark_name, self.config.split or "test", item_id, self.domain, str(row.get("Subdomain") or row.get("subdomain") or "science").strip().lower(), question, shuffled, answer, self.benchmark_type, {"source_record": dict(row)}))
        return self._apply_limit(items)


class ArcChallengeAdapter(HFAdapter):
    benchmark_name = "arc_challenge"
    domain = "science"
    benchmark_type = "multiple_choice"

    def load_examples(self) -> list[NormalizedExample]:
        dataset = self._load_hf_split() if not self.config.local_path else self._load_local_jsonl()
        items: list[NormalizedExample] = []
        for idx, row in enumerate(dataset):
            choice_bundle = row.get("choices") or {}
            labels = choice_bundle.get("label", []) if isinstance(choice_bundle, dict) else []
            texts = choice_bundle.get("text", []) if isinstance(choice_bundle, dict) else []
            ordered = [text for _, text in sorted(zip(labels, texts))] if labels else texts
            answer_key = str(row.get("answerKey") or row.get("answer") or "A").strip().upper()
            if answer_key.isdigit():
                answer_key = chr(ord("A") + int(answer_key) - 1)
            items.append(NormalizedExample(self.benchmark_name, self.config.split or "test", f"arc:{idx}", self.domain, "science", str(row.get("question") or row.get("prompt")).strip(), [str(text).strip() for text in ordered], answer_key, self.benchmark_type, {"source_record": dict(row)}))
        return self._apply_limit(items)


class MMLUProAdapter(HFAdapter):
    benchmark_name = "mmlu_pro"
    domain = "general_knowledge"
    benchmark_type = "multiple_choice"

    def load_examples(self) -> list[NormalizedExample]:
        dataset = self._load_hf_split() if not self.config.local_path else self._load_local_jsonl()
        items: list[NormalizedExample] = []
        for idx, row in enumerate(dataset):
            choices = [str(choice).strip() for choice in (row.get("options") or row.get("choices") or [])]
            answer = row.get("answer") if row.get("answer") is not None else row.get("answer_index")
            if isinstance(answer, int):
                answer = chr(ord("A") + answer)
            items.append(NormalizedExample(self.benchmark_name, self.config.split or "test", f"mmlu_pro:{idx}", self.domain, str(row.get("category") or row.get("subject") or "mmlu_pro").strip().lower(), str(row.get("question") or row.get("input")).strip(), choices, str(answer).strip().upper(), self.benchmark_type, {"source_record": dict(row)}))
        return self._apply_limit(items)


class MMLUReduxAdapter(HFAdapter):
    benchmark_name = "mmlu_redux_2"
    domain = "general_knowledge"
    benchmark_type = "multiple_choice"

    def load_examples(self) -> list[NormalizedExample]:
        if not self.config.local_path and self.config.subset is None:
            from datasets import get_dataset_config_names

            items: list[NormalizedExample] = []
            for subset in get_dataset_config_names(self.config.path or ""):
                scoped_config = type(self.config)(
                    key=self.config.key,
                    split=self.config.split,
                    path=self.config.path,
                    subset=subset,
                    local_path=self.config.local_path,
                    limit=self.config.limit,
                    shuffle=self.config.shuffle,
                    seed=self.config.seed,
                    trust_remote_code=self.config.trust_remote_code,
                    cache_dir=self.config.cache_dir,
                    extra_kwargs=dict(self.config.extra_kwargs),
                )
                scoped_adapter = MMLUReduxAdapter(scoped_config)
                items.extend(scoped_adapter.load_examples())
            return self._apply_limit(items)
        dataset = self._load_hf_split() if not self.config.local_path else self._load_local_jsonl()
        items: list[NormalizedExample] = []
        for idx, row in enumerate(dataset):
            choices = [str(choice).strip() for choice in (row.get("choices") or row.get("options") or [])]
            answer = row.get("answer") if row.get("answer") is not None else row.get("label")
            if isinstance(answer, int):
                answer = chr(ord("A") + answer)
            items.append(NormalizedExample(self.benchmark_name, self.config.split or "test", f"mmlu_redux:{idx}", self.domain, str(row.get("subject") or row.get("category") or "mmlu_redux").strip().lower(), str(row.get("question") or row.get("prompt")).strip(), choices, str(answer).strip().upper(), self.benchmark_type, {"source_record": dict(row)}))
        return self._apply_limit(items)


class HellaSwagAdapter(HFAdapter):
    benchmark_name = "hellaswag"
    domain = "commonsense"
    benchmark_type = "completion_choice"

    def load_examples(self) -> list[NormalizedExample]:
        dataset = self._load_hf_split() if not self.config.local_path else self._load_local_jsonl()
        items: list[NormalizedExample] = []
        for idx, row in enumerate(dataset):
            ctx = f"{row.get('ctx', '')} {row.get('ctx_b', '')}".strip()
            endings = [str(value).strip() for value in row.get("endings", [])]
            question = f"Complete the scenario naturally.\n\n{ctx}".strip()
            label = row.get("label", 0)
            answer = chr(ord("A") + int(label))
            items.append(NormalizedExample(self.benchmark_name, self.config.split or "validation", f"hellaswag:{idx}", self.domain, "commonsense_completion", question, endings, answer, self.benchmark_type, {"source_record": dict(row)}))
        return self._apply_limit(items)


class PIQAAdapter(HFAdapter):
    benchmark_name = "piqa"
    domain = "commonsense"
    benchmark_type = "multiple_choice"

    def load_examples(self) -> list[NormalizedExample]:
        dataset = self._load_hf_split() if not self.config.local_path else self._load_local_jsonl()
        items: list[NormalizedExample] = []
        for idx, row in enumerate(dataset):
            choices = [str(row.get("sol1")).strip(), str(row.get("sol2")).strip()]
            label = row.get("label", 0)
            answer = chr(ord("A") + int(label))
            items.append(NormalizedExample(self.benchmark_name, self.config.split or "validation", f"piqa:{idx}", self.domain, "physical_commonsense", str(row.get("goal") or row.get("question")).strip(), choices, answer, self.benchmark_type, {"source_record": dict(row)}))
        return self._apply_limit(items)


class BoolQAdapter(HFAdapter):
    benchmark_name = "boolq"
    domain = "factual_reading"
    benchmark_type = "yes_no"

    def load_examples(self) -> list[NormalizedExample]:
        dataset = self._load_hf_split() if not self.config.local_path else self._load_local_jsonl()
        items: list[NormalizedExample] = []
        for idx, row in enumerate(dataset):
            passage = str(row.get("passage") or "").strip()
            question = str(row.get("question") or "").strip()
            answer = "yes" if bool(row.get("answer")) else "no"
            items.append(NormalizedExample(self.benchmark_name, self.config.split or "validation", f"boolq:{idx}", self.domain, "reading_comprehension", f"Passage:\n{passage}\n\nQuestion: {question}".strip(), ["Yes", "No"], answer, self.benchmark_type, {"source_record": dict(row)}))
        return self._apply_limit(items)


class TruthfulQAMCAdapter(HFAdapter):
    benchmark_name = "truthfulqa_mc"
    domain = "factual_reading"
    benchmark_type = "multiple_choice"

    def load_examples(self) -> list[NormalizedExample]:
        dataset = self._load_hf_split() if not self.config.local_path else self._load_local_jsonl()
        items: list[NormalizedExample] = []
        for idx, row in enumerate(dataset):
            mc1_targets = row.get("mc1_targets") or {}
            choices = [str(choice).strip() for choice in mc1_targets.get("choices", [])]
            labels = list(mc1_targets.get("labels", []))
            answer_idx = labels.index(1) if 1 in labels else 0
            answer = chr(ord("A") + answer_idx)
            items.append(NormalizedExample(self.benchmark_name, self.config.split or "validation", f"truthfulqa:{idx}", self.domain, "truthfulness", str(row.get("question") or "").strip(), choices, answer, self.benchmark_type, {"source_record": dict(row)}))
        return self._apply_limit(items)


class FixtureMCQAdapter(HFAdapter):
    benchmark_name = "fixture_mcq"
    domain = "fixture"
    benchmark_type = "multiple_choice"

    def load_examples(self) -> list[NormalizedExample]:
        dataset = self._load_local_jsonl()
        items: list[NormalizedExample] = []
        for idx, row in enumerate(dataset):
            items.append(NormalizedExample(self.benchmark_name, self.config.split or "test", str(row.get("id") or f"fixture_mcq:{idx}"), str(row.get("domain") or self.domain), str(row.get("subdomain") or "fixture"), str(row.get("question")).strip(), [str(choice).strip() for choice in row.get("choices", [])], str(row.get("answer")).strip().upper(), self.benchmark_type, {"source_record": dict(row)}))
        return self._apply_limit(items)


class FixtureNumericAdapter(HFAdapter):
    benchmark_name = "fixture_numeric"
    domain = "fixture"
    benchmark_type = "numeric_boxed"

    def load_examples(self) -> list[NormalizedExample]:
        dataset = self._load_local_jsonl()
        items: list[NormalizedExample] = []
        for idx, row in enumerate(dataset):
            items.append(NormalizedExample(self.benchmark_name, self.config.split or "test", str(row.get("id") or f"fixture_numeric:{idx}"), str(row.get("domain") or self.domain), str(row.get("subdomain") or "fixture"), str(row.get("question")).strip(), None, str(row.get("answer")).strip(), self.benchmark_type, {"source_record": dict(row)}))
        return self._apply_limit(items)
