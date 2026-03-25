from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ModelSpec:
    key: str
    model_name: str
    family: str
    max_context_tokens: int | None = None


@dataclass(frozen=True, slots=True)
class BenchmarkSpec:
    key: str
    path: str | None
    subset: str | None
    split: str
    domain: str
    benchmark_type: str


MODEL_SPECS: dict[str, ModelSpec] = {
    "qwen25_7b_instruct": ModelSpec("qwen25_7b_instruct", "Qwen/Qwen2.5-7B-Instruct", "qwen25"),
    "llama31_8b_instruct": ModelSpec("llama31_8b_instruct", "meta-llama/Llama-3.1-8B-Instruct", "llama31"),
    "mistral7b_instruct_v03": ModelSpec("mistral7b_instruct_v03", "mistralai/Mistral-7B-Instruct-v0.3", "mistral7b"),
    "gemma2_9b_it": ModelSpec("gemma2_9b_it", "google/gemma-2-9b-it", "gemma2"),
    "phi4_mini_instruct": ModelSpec("phi4_mini_instruct", "microsoft/Phi-4-mini-instruct", "phi4"),
    "mistral_small_24b_instruct_2501": ModelSpec("mistral_small_24b_instruct_2501", "mistralai/Mistral-Small-24B-Instruct-2501", "mistral_small"),
    "deepseek_r1_distill_qwen_7b": ModelSpec("deepseek_r1_distill_qwen_7b", "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B", "deepseek_r1_distill_qwen"),
    "deepseek_r1_distill_llama_8b": ModelSpec("deepseek_r1_distill_llama_8b", "deepseek-ai/DeepSeek-R1-Distill-Llama-8B", "deepseek_r1_distill_llama"),
    "qwq_32b": ModelSpec("qwq_32b", "Qwen/QwQ-32B", "qwq"),
    "olmo2_1124_7b_instruct": ModelSpec("olmo2_1124_7b_instruct", "allenai/OLMo-2-1124-7B-Instruct", "olmo2"),
}


BENCHMARK_SPECS: dict[str, BenchmarkSpec] = {
    "gsm8k": BenchmarkSpec("gsm8k", "openai/gsm8k", "main", "test", "math", "numeric_boxed"),
    "math500": BenchmarkSpec("math500", "HuggingFaceH4/MATH-500", None, "test", "math", "numeric_boxed"),
    "gpqa": BenchmarkSpec("gpqa", "Idavidrein/gpqa", "gpqa_main", "train", "science", "multiple_choice"),
    "arc_challenge": BenchmarkSpec("arc_challenge", "allenai/ai2_arc", "ARC-Challenge", "test", "science", "multiple_choice"),
    "mmlu_pro": BenchmarkSpec("mmlu_pro", "TIGER-Lab/MMLU-Pro", None, "test", "general_knowledge", "multiple_choice"),
    "mmlu_redux_2": BenchmarkSpec("mmlu_redux_2", "edinburgh-dawg/mmlu-redux-2.0", None, "test", "general_knowledge", "multiple_choice"),
    "hellaswag": BenchmarkSpec("hellaswag", "Rowan/hellaswag", None, "validation", "commonsense", "completion_choice"),
    "piqa": BenchmarkSpec("piqa", "piqa", None, "validation", "commonsense", "multiple_choice"),
    "boolq": BenchmarkSpec("boolq", "google/boolq", None, "validation", "factual_reading", "yes_no"),
    "truthfulqa_mc": BenchmarkSpec("truthfulqa_mc", "truthfulqa/truthful_qa", "multiple_choice", "validation", "factual_reading", "multiple_choice"),
    "fixture_mcq": BenchmarkSpec("fixture_mcq", None, None, "test", "fixture_science", "multiple_choice"),
    "fixture_numeric": BenchmarkSpec("fixture_numeric", None, None, "test", "fixture_math", "numeric_boxed"),
}
