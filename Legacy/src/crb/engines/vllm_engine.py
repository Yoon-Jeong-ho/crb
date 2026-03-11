from __future__ import annotations

from crb.engines.base import InferenceEngine
from crb.schemas import DecodingConfig, ModelConfig
from crb.utils.runtime import resolve_tensor_parallel_size


class VllmEngine(InferenceEngine):
    def __init__(self, model_config: ModelConfig, decoding_config: DecodingConfig) -> None:
        from transformers import AutoTokenizer
        from vllm import LLM

        self.model_config = model_config
        self.decoding_config = decoding_config
        self.tensor_parallel_size = resolve_tensor_parallel_size(model_config.tensor_parallel_size)
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_config.model_name,
            trust_remote_code=model_config.trust_remote_code,
        )
        self.llm = LLM(
            model=model_config.model_name,
            trust_remote_code=model_config.trust_remote_code,
            tensor_parallel_size=self.tensor_parallel_size,
            dtype=model_config.dtype,
            max_model_len=model_config.max_model_len,
            gpu_memory_utilization=model_config.gpu_memory_utilization,
            download_dir=model_config.download_dir,
            enforce_eager=model_config.enforce_eager,
            swap_space=model_config.swap_space,
            max_num_seqs=model_config.max_num_seqs,
            seed=model_config.seed,
        )

    def generate(self, prompt: str) -> str:
        from vllm import SamplingParams

        sampling_params = SamplingParams(
            temperature=self.decoding_config.temperature,
            top_p=self.decoding_config.top_p,
            top_k=self.decoding_config.top_k,
            min_p=self.decoding_config.min_p,
            max_tokens=self.decoding_config.max_tokens,
            repetition_penalty=self.decoding_config.repetition_penalty,
            presence_penalty=self.decoding_config.presence_penalty,
            stop=self.decoding_config.stop or None,
        )
        output = self.llm.generate([prompt], sampling_params, use_tqdm=False)[0]
        return output.outputs[0].text.strip()

    def render_chat(self, messages: list[dict[str, str]]) -> str:
        template_kwargs = dict(self.model_config.chat_template_kwargs)
        if self.model_config.model_family.lower().startswith("qwen3") and "enable_thinking" not in template_kwargs:
            template_kwargs["enable_thinking"] = self.model_config.thinking_mode.lower() != "off"
        return self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            **template_kwargs,
        )

    def close(self) -> None:
        del self.llm
