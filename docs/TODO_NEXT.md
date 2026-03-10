# CRB Next TODO

## Highest priority
1. Run `configs/qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_off.yaml`
   - goal: get a clean GSM8K thinking off/on pair
2. Add a Qwen3-specific post-think answer extraction fallback for GPQA thinking-on
3. Revisit AIME parsing failure cases (`ambiguous_numeric_answer`)

## Medium priority
1. Increase GPQA thinking-off from smoke (`num_samples=8`) to a mini run
2. Increase AIME thinking-off from smoke (`num_samples=8`) to a mini run
3. Validate one thinking-on config on `CUDA_VISIBLE_DEVICES=6,7`
4. Launch a small materialized sweep subset for `k in {0,2,4,8}`

## Lower priority
1. Add more regression tests around GPQA deterministic choice shuffling
2. Add targeted tests for the numeric ambiguity fallback
3. Cleanly separate benchmark-result scoreboard rows from any future non-benchmark test artifacts

## Risks to track
- GPQA thinking-on may require parser changes, not just prompt changes
- AIME numeric ambiguity may inflate format failure if not handled explicitly
- Smoke-scale results are preliminary and should not yet be summarized as benchmark conclusions
