from __future__ import annotations

from transformers import AutoTokenizer

from crb_v2.config import ModelConfig
from crb_v2.engines.base import InferenceEngine


class VllmEngine(InferenceEngine):
    def __init__(self, model_config: ModelConfig) -> None:
        from vllm import LLM

        self.model_config = model_config
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_config.model_name,
            trust_remote_code=model_config.trust_remote_code,
        )
        tp = model_config.tensor_parallel_size
        if isinstance(tp, str) and tp == "auto":
            import os
            visible = os.environ.get("CUDA_VISIBLE_DEVICES", "")
            tp = max(1, len([item for item in visible.split(",") if item.strip()]))
        self.llm = LLM(
            model=model_config.model_name,
            trust_remote_code=model_config.trust_remote_code,
            tensor_parallel_size=int(tp),
            dtype=model_config.dtype,
            max_model_len=model_config.max_context_tokens,
            gpu_memory_utilization=model_config.gpu_memory_utilization,
            download_dir=model_config.download_dir,
            enforce_eager=model_config.enforce_eager,
            swap_space=model_config.swap_space,
            max_num_seqs=model_config.max_num_seqs,
            seed=model_config.seed,
        )

    def generate(self, prompt: str, request_options: dict | None = None) -> str:
        from vllm import SamplingParams
        from vllm.sampling_params import StructuredOutputsParams

        request_options = request_options or {}
        structured_choice = request_options.get("structured_choice") or None
        structured_regex = request_options.get("structured_regex") or None
        structured_outputs = None
        if structured_choice or structured_regex:
            structured_outputs = StructuredOutputsParams(choice=structured_choice, regex=structured_regex)
        params = SamplingParams(
            temperature=self.model_config.temperature,
            top_p=self.model_config.top_p,
            top_k=self.model_config.top_k,
            min_p=self.model_config.min_p,
            max_tokens=self.model_config.max_new_tokens,
            repetition_penalty=self.model_config.repetition_penalty,
            presence_penalty=self.model_config.presence_penalty,
            stop=self.model_config.stop or None,
            structured_outputs=structured_outputs,
        )
        output = self.llm.generate([prompt], params, use_tqdm=False)[0]
        return output.outputs[0].text.strip()

    def count_tokens(self, prompt: str) -> int:
        return len(self.tokenizer.encode(prompt))

    @property
    def tokenizer_model_limit(self) -> int | None:
        value = getattr(self.tokenizer, "model_max_length", None)
        return value if isinstance(value, int) else None

    def close(self) -> None:
        del self.llm
