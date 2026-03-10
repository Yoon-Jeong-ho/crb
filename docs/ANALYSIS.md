# CRB Analysis

## Scope
This document summarizes the current **preliminary** smoke-scale CRB results for the newly added Qwen3 / GPQA / GSM8K / AIME paths. These are not yet paper-scale conclusions.

## Current smoke results

### 1. GPQA with Qwen3 thinking off
- Config: `qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off`
- `num_samples=8`
- Accuracy: `0.500`
- Format failure rate: `0.000`

Interpretation:
- The thinking-off path is operational and format-stable on this small GPQA setting.
- This is the cleanest current baseline for reasoning-mode comparison.

### 2. GPQA with Qwen3 thinking on
- Config: `qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on`
- `num_samples=8`
- Accuracy: `0.125`
- Format failure rate: `0.875`

Interpretation:
- The dominant issue is **format collapse**, not just lower answer quality.
- In this smoke run, the model often emitted long `<think>` traces without a parseable canonical final-answer line.
- Only `1/8` items parsed cleanly.

### 3. GPQA with Qwen3 thinking on + stricter final-answer instruction
- Config: `qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_strictfinal`
- `num_samples=8`
- Accuracy: `0.000`
- Format failure rate: `1.000`

Interpretation:
- A prompt-only rescue attempt did **not** help.
- In this smoke run it made parsing worse.
- This suggests the failure is not trivially solvable by tightening the visible final-answer instruction alone.

### 4. GSM8K with Qwen3 thinking on
- Config: `qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_on`
- `num_samples=8`
- Accuracy: `0.125`
- Format failure rate: `0.125`

Interpretation:
- Thinking-on remains weak in answer quality in this small sample.
- However, formatting is **far more stable** than GPQA thinking-on.
- This suggests the severe GPQA issue is condition-specific rather than a universal Qwen3 thinking-on parser failure.

### 5. AIME with Qwen3 thinking off
- Config: `qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off`
- `num_samples=8`
- Accuracy: `0.125`
- Format failure rate: `0.250`
- Parsed items: `6/8`
- Invalid items: `2/8`
- Dominant invalid reason: `ambiguous_numeric_answer`

Interpretation:
- The AIME adapter and numeric evaluator are working end-to-end.
- The failure mode is mostly numeric ambiguity, not total parser collapse.

### 6. Multi-GPU smoke validation
- Config: `qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_multigpu_smoke`
- `num_samples=2`
- GPUs: `6,7`
- Accuracy: `0.500`
- Format failure rate: `0.000`

Interpretation:
- The new Qwen3 GPQA path is verified on both execution routes:
  - single GPU (`6`)
  - multi GPU (`6,7`)

## Comparison summary

### Qwen3 thinking off vs on
Current evidence suggests:
- **thinking off**: stable formatting on GPQA, reasonable smoke baseline
- **thinking on**: drastically worse formatting on GPQA, but much less severe parser instability on GSM8K

This means the “thinking on” effect is likely interacting with:
- task type
- prompt structure
- maybe multi-turn scientific MCQ formatting in particular

### GPQA vs GSM8K vs AIME
- **GPQA**: strongest exposure of visible-format failure under thinking-on
- **GSM8K**: thinking-on still inaccurate, but parser mostly survives
- **AIME**: numeric path works; main issue is ambiguous multiple-number outputs

## Failure modes observed

1. **Thinking-trace spillover**
   - Qwen3 thinking-on often leaves a long reasoning trace without a clean canonical final-answer line.

2. **Prompt-only rescue failure**
   - Stricter final-answer wording alone did not fix GPQA thinking-on.

3. **Ambiguous numeric outputs**
   - AIME outputs sometimes contain multiple plausible integers in the final text.

4. **Manifest construction dependency on cross-domain availability**
   - AIME initially failed because the config did not include enough non-math dummy sources for the cross-domain manifest branch.

## Practical takeaways right now
- GPQA + Qwen3 thinking-off is currently usable as a CRB smoke path.
- GPQA + Qwen3 thinking-on is not yet robust enough for paper-scale use without additional handling.
- GSM8K is a better next target for studying Qwen3 thinking-on because the parser is not collapsing as badly.
- AIME can stay in the benchmark set now; the adapter/evaluator path is valid.

## What is still missing before paper-scale claims
- larger `num_samples`
- Qwen3 thinking-off / thinking-on paired comparison on GSM8K
- broader comparisons across `k={0,2,4,8}`
- explicit self-history/oracle-history comparisons beyond the current smoke set
- stronger strategy for thinking-on answer extraction on GPQA

## Recommended next experiments
1. Run Qwen3 thinking-off on GSM8K for a clean on/off pair
2. Try a parser-side fallback that extracts the **last** valid `Answer:` line after `<think>` blocks for GPQA thinking-on
3. Increase GPQA thinking-off and AIME thinking-off from smoke to mini runs
4. Launch a materialized sweep subset rather than the entire 256-config matrix at once
