# CRB Analysis

## Scope
This document summarizes the current **full-sample main-table state** for Qwen3-1.7B across GPQA, GSM8K, AIME, and MMLU.

## Current verified full-sample conditions

### GPQA / Qwen3 / k=2 / multi_turn / oracle_history / same_domain
- thinking off (`num_items=448`): accuracy `0.27232142857142855`, format failure `0.008928571428571428`
- thinking on with `/no_think` + prefill (`num_items=448`): accuracy `0.27232142857142855`, format failure `0.026785714285714284`

Interpretation:
- The earlier GPQA thinking-on format collapse has been removed at full scale.
- However, the new thinking-on path does **not** improve accuracy over thinking off.
- The tradeoff is now “comparable accuracy, slightly worse format robustness,” rather than catastrophic parse failure.

### GSM8K / Qwen3 / k=2 / single_turn_flattened / self_history / cross_domain
- thinking off (`num_items=1319`): accuracy `0.35178165276724793`, format failure `0.18271417740712662`
- thinking on (`num_items=1319`): accuracy `0.3889310083396513`, format failure `0.1379833206974981`

Interpretation:
- This is the clearest current full-sample win for thinking on.
- Thinking on improves both answer quality and output-format robustness in this condition.
- GSM8K remains the strongest benchmark for showing that thinking-on behavior is not uniformly harmful.

### AIME / Qwen3 / k=2 / multi_turn / oracle_history / same_domain
- thinking off (`num_items=30`): accuracy `0.1`, format failure `0.26666666666666666`
- thinking on (`num_items=30`): accuracy `0.03333333333333333`, format failure `0.8333333333333334`

Interpretation:
- AIME thinking-on is currently unstable and not ready for use as a strong main-table comparison row.
- The dominant issue is again output-format failure, but here the accuracy also worsens sharply.

## Direct-pair summary
Current canonical direct pairs from `results/analysis/main_table_qwen3.csv`:

1. **GPQA**
   - off vs on accuracy delta: `0.0000`
   - off vs on format-failure delta: `+0.0179` for thinking on

2. **GSM8K**
   - off vs on accuracy delta: `+0.0371` for thinking on
   - off vs on format-failure delta: `-0.0447` for thinking on

3. **AIME**
   - off vs on accuracy delta: `-0.0667` for thinking on
   - off vs on format-failure delta: `+0.5667` for thinking on

## Main findings

### Finding 1: the GPQA thinking-on path is now usable, but not better
The `/no_think` + prefill control moved GPQA thinking-on from “broken” to “usable.”
That is a meaningful infrastructure/result quality win.
But at full scale, it lands at the same accuracy as thinking off and slightly worse format failure.

### Finding 2: GSM8K provides the strongest current argument for reasoning-mode sensitivity
On GSM8K, thinking on improves both metrics at full scale.
This makes GSM8K the best current benchmark for a positive thinking-on result in CRB.

### Finding 3: AIME thinking-on remains the weakest lane
AIME thinking-on should not yet be promoted into broader sweep claims.
Its current full-sample row is too format-unstable.

### Finding 4: the main table is now full-sample for four benchmarks
GPQA, GSM8K, AIME, and MMLU now have full-sample canonical rows.
This is a clear step up from the earlier smoke/mini regime.

## MMLU / Qwen3 / k=2 / multi_turn / oracle_history / same_domain
- thinking off (`num_items=14042`): accuracy `0.5883777239709443`, format failure `0.0010682238997293833`
- thinking on (`num_items=14042`): accuracy `0.6664292835778379`, format failure `0.021364477994587665`

Interpretation:
- MMLU is now the strongest broad-coverage benchmark in the repository.
- Thinking on improves accuracy substantially at full scale here, while remaining highly parseable.
- The cost is a small format-failure increase, but it stays very low in absolute terms.

## What is paper-usable now
- full-sample GPQA off/on row
- full-sample GSM8K off/on row
- full-sample AIME off/on row
- canonical `main_table_qwen3.csv/json` artifacts
- k-aware pair aggregation that no longer collapses different `k` conditions into one row

## What still needs work
1. Add a per-dataset error taxonomy on the finished four-benchmark table.
2. Start selective k-sweep expansion from the strongest current rows.
3. Revisit AIME thinking-on only if we want broader “thinking on/off everywhere” claims.
4. Decide whether the headline table should emphasize the positive GSM8K/MMLU thinking-on effect or the mixed benchmark sensitivity story.
