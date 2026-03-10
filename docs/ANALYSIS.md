# CRB Analysis

## Scope
This document summarizes the current **preliminary** smoke-scale CRB results for the newly added Qwen3 / GPQA / AIME paths. These are not yet paper-scale conclusions.

## Current smoke results

### 1. GPQA with Qwen3 thinking off
- Config: `qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off`
- `num_samples=8`
- Accuracy: `0.500`
- Format failure rate: `0.000`

Interpretation:
- The thinking-off path is operational and format-stable on this small GPQA setting.
- This is a useful baseline for comparing reasoning-mode interference and formatting behavior.

### 2. GPQA with Qwen3 thinking on
- Config: `qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on`
- `num_samples=8`
- Accuracy: `0.125`
- Format failure rate: `0.875`

Interpretation:
- The major difference is not just lower accuracy; it is a **format collapse**.
- In this smoke run, the model often emitted long `<think>` traces without a clean final canonical answer line.
- As a result, only `1/8` items were parsed successfully.

Preliminary takeaway:
- For this exact GPQA + multi-turn + oracle-history + same-domain + k=2 condition, the current Qwen3 thinking-on configuration is much less parser-stable than thinking-off.
- Before paper-scale sweeps, we likely need either:
  1. a stricter answer-only instruction,
  2. a Qwen3-specific final-answer extraction fallback,
  3. a different thinking-on decoding setting, or
  4. a second benchmark check (e.g. GSM8K) to determine whether the issue is GPQA-specific.

### 3. AIME with Qwen3 thinking off
- Config: `qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off`
- `num_samples=8`
- Accuracy: `0.125`
- Format failure rate: `0.250`
- Parsed items: `6/8`
- Invalid items: `2/8`
- Dominant invalid reason: `ambiguous_numeric_answer`

Interpretation:
- The AIME adapter and numeric evaluator are working end-to-end.
- Numeric parsing is meaningfully functional, but some outputs contain multiple competing numeric candidates.
- This is a pipeline success with model-quality limitations and some parser ambiguity still exposed.

## Comparison summary

### Qwen3 thinking off vs on
Current evidence from GPQA smoke runs suggests:
- thinking off: stable formatting, moderate smoke accuracy
- thinking on: severe formatting degradation, much lower measured accuracy

This is currently the strongest signal in the new results.

### GPQA vs AIME
- GPQA exposes **format instability** strongly under thinking-on.
- AIME exposes **numeric ambiguity** even when the final answer is often parseable.

This suggests the two benchmarks stress different failure modes:
- GPQA: output-structure / canonical-answer compliance
- AIME: numeric-answer isolation / ambiguity

## Failure modes observed

1. **Thinking-trace spillover**
   - Qwen3 thinking-on often leaves a long reasoning trace without a final canonical answer line.

2. **Ambiguous numeric outputs**
   - AIME outputs sometimes contain multiple plausible integers in the final text.

3. **Manifest construction dependency on cross-domain availability**
   - AIME initially failed because the config did not include enough non-math dummy sources for the cross-domain manifest branch.

## What is still missing before paper-scale claims
- larger `num_samples`
- Qwen3 thinking-on validation on GSM8K
- multi-GPU validation for the new Qwen3 configs
- broader comparisons across `k={0,2,4,8}`
- explicit self-history/oracle-history comparisons beyond the current smoke set

## Recommended next experiments
1. Qwen3 thinking-on on GSM8K to test whether parser collapse is GPQA-specific
2. AIME prompt/parser refinement to reduce `ambiguous_numeric_answer`
3. GPQA mini-run with thinking-off and thinking-on after prompt tightening
4. Begin materialized paper sweep generation for controlled next-batch execution
