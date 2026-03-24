# Experiment Matrix

## Models

- `qwen25_7b_instruct`
- `llama31_8b_instruct`
- `mistral7b_instruct_v03`
- `gemma2_9b_it`
- `phi4_mini_instruct`
- `mistral_small_24b_instruct_2501`
- `deepseek_r1_distill_qwen_7b`
- `deepseek_r1_distill_llama_8b`
- `qwq_32b`
- `olmo2_1124_7b_instruct`

## Benchmarks

- `gsm8k`
- `math500`
- `gpqa`
- `arc_challenge`
- `mmlu_pro`
- `mmlu_redux_2`
- `hellaswag`
- `piqa`
- `boolq`
- `truthfulqa_mc`

## Sweep axes

- `k`: `0, 2, 4, 8, 16, 32`
- `relation`: `same_benchmark`, `same_domain_other_benchmark`, `cross_domain`
- `provenance`: `model_correct`, `model_incorrect`, `oracle`

## Configs

- smoke: `configs_v2/pilot/mock_fixture_smoke.yaml`
- pilot template: `configs_v2/pilot/two_models_two_benchmarks.yaml`
- full matrix template: `configs_v2/full/full_matrix.yaml`
