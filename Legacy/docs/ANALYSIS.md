# CRB Analysis

## Scope
This document summarizes the current **preliminary** staged CRB results for Qwen3 across GPQA, GSM8K, and AIME. Some results are smoke-scale; GPQA thinking-off and AIME thinking-off now also have mini-run follow-up coverage.

## Current verified conditions

### GPQA / Qwen3 / thinking off
- smoke (`num_samples=8`): accuracy `0.500`, format failure `0.000`
- mini (`num_samples=32`): accuracy `0.40625`, format failure `0.000`

Interpretation:
- The main result is stability, not raw absolute accuracy.
- GPQA thinking-off is parser-stable and therefore suitable as a baseline path for larger CRB sweeps.
- The slight drop from `0.500` to `0.40625` with more samples is unsurprising and does not indicate a pipeline problem.

### GPQA / Qwen3 / thinking on
- canonical smoke (`num_samples=8`): accuracy `0.125`, format failure `0.875`
- strict-final rescue attempt (`num_samples=8`): accuracy `0.000`, format failure `1.000`

Interpretation:
- The failure mode is still dominated by formatting rather than purely wrong answers.
- The stricter final-answer prompt did not help, which suggests a parser/postprocessing or generation-budget issue rather than a simple instruction clarity issue.
- Many outputs appear to spend the entire visible budget in reasoning text and never surface a final canonical line.

### GSM8K / Qwen3 off/on direct pair
- thinking off (`num_samples=8`): accuracy `0.375`, format failure `0.250`
- thinking on (`num_samples=8`): accuracy `0.125`, format failure `0.125`

Interpretation:
- On GSM8K, thinking-on is still weak on answer quality in the current small run, but parser stability is much better than GPQA.
- That strongly suggests the GPQA thinking-on problem is not just a universal “thinking-on breaks the parser” phenomenon.

### AIME / Qwen3 / thinking off
- smoke (`num_samples=8`): accuracy `0.125`, format failure `0.250`
- mini (`num_samples=16`): accuracy `0.125`, format failure `0.250`

Interpretation:
- The benchmark path is stable enough to reuse.
- The evaluator works; the dominant failure is not infrastructure failure but numeric ambiguity / wrong answers.
- The unchanged metrics across smoke and mini suggest the issue is persistent model behavior rather than noise from the very small sample.

## Direct pair summary
Current canonical direct pairs from `results/analysis/direct_qwen3_pairs.csv`:

1. **GPQA / multi_turn / oracle_history / same_domain / k=2**
   - off: accuracy `0.40625`, format failure `0.000`
   - on: accuracy `0.125`, format failure `0.875`

2. **GSM8K / single_turn_flattened / self_history / cross_domain / k=2**
   - off: accuracy `0.375`, format failure `0.250`
   - on: accuracy `0.125`, format failure `0.125`

## Main provisional findings

### Finding 1: GPQA is the most sensitive current probe for reasoning-mode instability
GPQA with thinking-on is currently the sharpest failure detector in the repository:
- parser stability collapses
- answer quality also drops
- prompt-only rescue did not fix it

### Finding 2: thinking-on instability is condition-specific, not globally uniform
GSM8K thinking-on remains parseable in most cases.
Therefore, the GPQA failure seems to depend on benchmark/task structure rather than just “thinking on” by itself.

### Finding 3: AIME is ready to remain in the benchmark suite
AIME adapter + numeric evaluator + manifest handling are now verified repeatedly.
The remaining problem is quality/ambiguity, not pipeline readiness.

### Finding 4: multi-GPU support for the new Qwen3 path is validated
At least one new GPQA path now works on `CUDA_VISIBLE_DEVICES=6,7`, which reduces risk before wider sweep expansion.

## Failure modes observed

1. **Reasoning spillover / no final answer surfaced**
   - especially GPQA thinking-on
2. **Prompt-only rescue failure**
   - strict final-answer wording alone was ineffective
3. **Ambiguous numeric outputs**
   - especially AIME
4. **Manifest dependence on cross-domain candidate diversity**
   - already fixed in the AIME config

## What becomes paper-usable now
- GPQA thinking-off path
- GSM8K off/on comparison path
- AIME benchmark inclusion path
- scoreboard / JSON / metadata pipeline
- direct-pair aggregation artifacts in `results/analysis/`

## What still needs work before broader sweep claims
- parser/postprocessing strategy for GPQA thinking-on
- larger direct-pair runs on GSM8K and GPQA
- first selective sweep subset across `k={0,2,4,8}`
- more history/domain comparison coverage beyond isolated conditions

## Recommended next experiments
1. Implement a parser/postprocessing fallback specifically for GPQA thinking-on outputs
2. Launch a selective generated-sweep subset focused on:
   - GPQA thinking-off across `k={0,2,4,8}`
   - GSM8K off/on pair continuation
3. Expand GPQA thinking-off and AIME thinking-off one more step if compute budget allows
4. Validate a thinking-on path on multi-GPU
