# CRB Paper Results Summary (2026-03-15)

## 1. What this benchmark is trying to measure

CRB is not primarily a reasoning-mode benchmark. Its primary object is **conversation-accumulated interference**:

- prepend `k` dummy turns before a final target question
- vary whether that history is rendered as real turns or flattened text
- vary whether the dummy answers are gold (`oracle_history`) or the model's own previous answers (`self_history`)
- vary whether the dummy answers are explicitly wrong (`wrong_history`)
- vary whether the dummy items are from the same domain or a different domain
- score **only the final target answer**

In this framing, `thinking on/off` is a **secondary analysis axis** layered on top of the main accumulated-history protocol.

As of 2026-03-15, CRB also has an explicit `wrong_history` axis so that:
- **correct dummy answers** (`oracle_history`)
- **model-produced previous answers** (`self_history`)
- **controlled incorrect dummy answers** (`wrong_history`)
can be compared directly.

## 2. Full-sample main table

The current full-sample main table uses one canonical row per benchmark.

| Dataset | Condition | Off Acc | On Acc | Off FF | On FF | N |
|---|---|---:|---:|---:|---:|---:|
| GPQA | multi_turn / oracle_history / same_domain / k=2 | 0.2723 | 0.2723 | 0.0089 | 0.0268 | 448 |
| GSM8K | single_turn_flattened / self_history / cross_domain / k=2 | 0.3518 | 0.3889 | 0.1827 | 0.1380 | 1319 |
| AIME | multi_turn / oracle_history / same_domain / k=2 | 0.1000 | 0.0333 | 0.2667 | 0.8333 | 30 |
| MMLU | multi_turn / oracle_history / same_domain / k=2 | 0.5884 | 0.6664 | 0.0011 | 0.0214 | 14042 |

`FF` = `format_failure_rate`

### Main-table interpretation

- **MMLU**: strongest positive thinking-on result. Accuracy rises by about **+7.8 points**, while format failure remains very low in absolute terms.
- **GSM8K**: also clearly positive for thinking on. Accuracy improves by about **+3.7 points** and format failure drops.
- **GPQA**: thinking-on no longer catastrophically collapses after the `/no_think + prefill` rescue, but it does **not** outperform thinking off at full scale.
- **AIME**: thinking-on remains a clear failure case under the current setup; both accuracy and format stability worsen.

## 3. Broad sweep status

The full generated `qwen3_core_paper` sweep completed.

- total generated Qwen3 sweep rows: **256**
- paired off/on conditions: **128**
- each generated config uses **50 samples**

This means the repo now has:
- a **full-sample four-benchmark main table**, and
- a **broad 256-condition sweep** for analyzing the protocol axes.

## 4. Sweep-wide findings

### 4.1 Average on-off effect by dataset

Across the 128 paired conditions in the generated sweep, the mean accuracy deltas (`on - off`) are:

- **AIME**: `+0.0172`, but with a very large format-failure increase (`+0.2828`)
- **GPQA**: `-0.0419`, with worse format failure (`+0.2156`)
- **GSM8K**: `+0.2469`, with a slight format-failure increase on average (`+0.0256`)
- **MMLU**: `+0.1062`, with a small format-failure increase (`+0.0244`)

### 4.2 Average protocol effects over the sweep

Average accuracy / format failure over all 256 generated rows:

- `multi_turn`: acc `0.3588`, ff `0.2002`
- `single_turn_flattened`: acc `0.2910`, ff `0.1344`
- `oracle_history`: acc `0.3221`, ff `0.1663`
- `self_history`: acc `0.3277`, ff `0.1683`
- `cross_domain`: acc `0.3207`, ff `0.1841`
- `same_domain`: acc `0.3291`, ff `0.1505`

### 4.3 Average k effect over the sweep

Average accuracy by `k` across all generated rows:

- `k=0`: acc `0.3556`
- `k=2`: acc `0.3189`
- `k=4`: acc `0.3228`
- `k=8`: acc `0.3022`

This is not perfectly monotonic, but the overall pattern is still consistent with the main CRB hypothesis: **more accumulated dummy history tends to degrade final-target performance**.

## 5. Canonical k-sweep readout for the strongest benchmark rows

### MMLU / multi_turn / oracle_history / same_domain
- off: `(k=0,2,4,8) = 0.46, 0.42, 0.48, 0.42`
- on: `(k=0,2,4,8) = 0.62, 0.74, 0.62, 0.56`

### GSM8K / single_turn_flattened / self_history / cross_domain
- off: `(k=0,2,4,8) = 0.58, 0.40, 0.42, 0.30`
- on: `(k=0,2,4,8) = 0.60, 0.44, 0.44, 0.40`

### GPQA / multi_turn / oracle_history / same_domain
- off: `(k=0,2,4,8) = 0.28, 0.36, 0.34, 0.38`
- on: `(k=0,2,4,8) = 0.16, 0.20, 0.12, 0.18`
- GPQA thinking-on still has much higher format failure than off across the same lane.

### AIME / multi_turn / oracle_history / same_domain
- off: `(k=0,2,4,8) = 0.10, 0.10, 0.05, 0.05`
- on: `(k=0,2,4,8) = 0.05, 0.05, 0.10, 0.15`
- However, AIME thinking-on remains highly format-unstable, so raw accuracy alone should not be over-interpreted.

## 6. Main paper takeaway

The current results support the following interpretation:

1. **CRB is fundamentally a dummy-history interference benchmark**, not a pure reasoning-mode benchmark.
2. Accumulated history effects are real and visible when moving from `k=0` to larger `k` values.
3. The effect of `thinking on/off` is **benchmark-dependent**:
   - positive on **MMLU** and **GSM8K**,
   - roughly neutral after rescue on **GPQA**,
   - negative on **AIME**.
4. Therefore, reasoning mode should be treated as a **secondary moderator** of history interference, not the main story.

## 7. Strongest current claims

The most defensible current claims are:

- accumulated dummy history changes final-target accuracy in measurable ways
- the shape of that degradation depends on dataset and protocol axis
- broad knowledge (`MMLU`) and arithmetic reasoning (`GSM8K`) can benefit from thinking-on
- hard science MCQ (`GPQA`) is much more sensitive to answer-emission stability
- hard numeric competition math (`AIME`) remains the weakest current lane for thinking-on

## 8. Limits / caution points

- Many broader sweep rows use `n=50`, so they are good for trend detection but not for final high-confidence headline numbers by themselves.
- AIME has only `30` items in the full table and remains highly format-sensitive.
- GPQA thinking-on required a rescue control (`/no_think + prefill`), so it should not be presented as a simple “vanilla thinking-on” success case.
- The protocol-level averages should not be over-read without item-level paired analysis.

## 9. Best next paper steps

1. Add **item-level paired delta** analysis for `k=0 -> 2 -> 4 -> 8`.
2. Add **accuracy vs format-failure decomposition** per dataset.
3. Build one figure each for:
   - canonical `k` sweep
   - `multi_turn vs flattened`
   - `oracle_history vs self_history vs wrong_history`
   - `same_domain vs cross_domain`
4. Treat `thinking on/off` as a second-layer table/figure, not the main benchmark definition.

## 10. Current protocol-first follow-up runs

The current selective full-sample follow-ups are:

- **GPQA / oracle_history / same_domain / k={0,4,8}** — completed
- **GPQA / wrong_history / same_domain / k={2,4,8}** — completed
- **GSM8K / self_history / cross_domain / k={0,4,8}** — in progress
- **GSM8K / wrong_history / cross_domain / k={2,4,8}** — in progress
