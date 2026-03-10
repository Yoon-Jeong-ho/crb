# CRB Next TODO

## Highest priority
1. Run `configs/qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_on.yaml`
   - goal: check whether thinking-on format failure is GPQA-specific or general
2. Compare GPQA thinking-on vs thinking-off with a stricter final-answer instruction variant
3. Revisit AIME parsing failure cases (`ambiguous_numeric_answer`)

## Medium priority
1. Increase GPQA and AIME from smoke (`num_samples=8`) to mini runs
2. Validate one new Qwen3 config on `CUDA_VISIBLE_DEVICES=6,7`
3. Materialize `configs/sweeps/qwen3_core_paper.yaml`
4. Launch k=0 and k=4 follow-ups for GPQA

## Lower priority
1. Add Qwen3 thinking-on/off coverage to GSM8K and MMLU paper templates more explicitly in README examples
2. Add additional tests for GPQA deterministic choice shuffling and AIME numeric normalization edge cases
3. Add a Qwen3-specific parser fallback for outputs containing `<think>` blocks and no clean final line

## Risks to track
- Qwen3 thinking-on may require special parsing or stricter prompting before paper-scale use
- AIME numeric ambiguity may inflate format failure if not handled explicitly
- Smoke-scale results are preliminary and should not yet be summarized as benchmark conclusions
