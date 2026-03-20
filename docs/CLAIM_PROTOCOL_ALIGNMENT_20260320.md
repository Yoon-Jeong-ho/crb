# Claim + Protocol Alignment

- Date: 2026-03-20
- Status: **claim-first freeze; do not widen experiment scope until docs/results are re-aligned**

## Why CRB exists

CRB is **not** trying to create a new generic multi-turn task or score “chat quality.”

CRB exists to:

> keep the original single-turn benchmark target item fixed,  
> prepend accumulated dummy conversation history,  
> and measure how much the **final target answer** changes under that history.

The core object is therefore:

**target-only scoring under accumulated conversation history**

or, more compactly:

**conversation-accumulated robustness**.

## Current primary goal

The current primary goal is:

**establish a paper-worthy CRB protocol and main claim**.

That means showing:

1. single-turn benchmark accuracy alone does not capture conversational robustness,
2. accumulated prior turns can change final-target accuracy even when the target item itself is unchanged,
3. the effect depends on the **type of history**, not only on added length.

Model ranking and Qwen3-specific debugging are secondary to that goal.

## Story freeze: main / supporting / appendix

### Main figure / main story

**Multimodel `stored_history` / external contamination**

Use this as the headline because it most directly supports:

- the existence of a conversation-accumulated robustness axis beyond single-turn accuracy,
- cross-model generalization,
- a cleaner comparison surface than model-specific self-history trajectories.

### Main supporting analysis

**Qwen3 / GPQA / multi_turn / oracle-vs-wrong-vs-stored provenance**

Use this as the controlled provenance readout:

- how history provenance changes final-target behavior,
- in a hard benchmark,
- under actual multi-turn structure.

### Appendix / exploratory branch

**Qwen3 / GSM8K / thinking-on / flattened / self-vs-wrong**

Keep this as:

- exploratory self-contamination evidence,
- useful but not headline-safe due to remaining interpretation risk from thinking-on and flattened-only structure.

## Canonical baseline

All degradation calculations should now use one canonical baseline:

**`single_turn`, `k=0`, no dummy history**

Use:

`Delta(condition) = Acc(condition) - Acc(single_turn k=0)`

Other comparisons remain useful, but only as secondary readouts:

- `multi_turn k=0` vs `single_turn k=0`
- within-slice `k` trends
- `self` vs `stored` vs `oracle` vs `wrong`

## Main protocol axes

The current main story should be organized around these axes:

1. **Baseline**
   - `single_turn`, `k=0`
2. **Structure**
   - `multi_turn` vs `single_turn_flattened`
3. **Provenance**
   - `self_history`
   - `oracle_history`
   - `wrong_history`
   - `stored_history`
4. **Relation**
   - `same_benchmark` / same-dataset same-domain
   - `same_domain_other_dataset`
   - `cross_domain`
5. **History size**
   - `k`

## Interpretation freeze for `stored_history`

`stored_history` is **not** a full replacement for `self_history`.

Use the following interpretation:

- `self_history`
  - the model sequentially accumulates its own prior answers
  - measures **self-contamination / self-accumulation**
- `stored_history`
  - a precomputed history pool is injected before the target
  - measures **externally supplied contaminated-history robustness**

Therefore:

- do **not** write `stored_history` as if it were just a scalable `self_history` proxy,
- do treat it as a separate controlled condition that helps isolate the effect of history provenance.

## Current artifact classification

### A. Directly useful for the main claim

These are the strongest currently available families of evidence.

#### 1. Canonical single-turn baselines

Full-sample `single_turn, k=0` baselines exist for:

- `qwen3`
  - `gpqa` off/on
  - `gsm8k` off/on
  - `aime` off/on
  - `mmlu` off/on
- `qwen25`
  - `gpqa`, `gsm8k`, `aime`, `mmlu` off
- `llama32_3b`
  - `gpqa`, `gsm8k`, `aime`, `mmlu` off
- `mistral7b`
  - `gpqa`, `gsm8k`, `aime`, `mmlu` off

These are the anchor rows for all headline deltas.

#### 2. Qwen3 full-sample provenance / contamination slices

- `qwen3/gpqa/off`
  - `multi_turn + oracle_history + same_domain`
  - `multi_turn + wrong_history + same_domain`
  - `multi_turn + stored_history + same_domain/cross_domain`
- `qwen3/gpqa/on`
  - `multi_turn + oracle_history + same_domain`
  - `multi_turn + stored_history + same_domain`
- `qwen3/gsm8k/off`
  - `single_turn_flattened + self_history + cross_domain`
  - `multi_turn + stored_history + cross_domain`
- `qwen3/gsm8k/on`
  - `single_turn_flattened + self_history + cross_domain`
  - `single_turn_flattened + wrong_history + cross_domain`
- `qwen3/mmlu/off/on`
  - `multi_turn + oracle_history + same_domain` full-sample comparison against `single_turn k=0`
- `qwen3/aime/off/on`
  - limited but still directly aligned full-sample baseline + same-domain follow-up rows

#### 3. Multimodel external-contamination slice

For `qwen25`, `llama32_3b`, and `mistral7b`, full-sample baselines plus full-sample `stored_history` follow-ups now exist across:

- `gpqa`
- `gsm8k`
- `aime`
- `mmlu`

with relation conditions including:

- `same_domain`
- `same_domain_other_dataset` where meaningful
- `cross_domain`

This is the strongest current evidence for:

**external contaminated-history robustness generalizing beyond Qwen3**.

### B. Secondary / supporting / implementation-focused

Keep these, but do not make them the paper headline:

- Qwen3 GPQA parserfix / strict-final / choice-constrained / `/no_think + prefill` runs
- single-turn pool collection itself
- workflow materialization scripts
- 50-item pilot sweeps that are useful for mechanism scouting but not headline tables
- mock / fixture validation runs

These are important for pipeline stability and slice selection, but they are not the main CRB claim.

### C. Exclude or park for now

These should not be used as headline evidence until cleaned up or explicitly reclassified:

- partial-only runs without final JSON + scoreboard row
- stale derived analysis files that do not reflect the current scoreboard
- the known missing-result legacy row:
  - `run-20260310T060638Z-8018d675`

As of 2026-03-20:

- `Legacy/results/summary/scoreboard.csv` has **573** rows
- `analysis/tables/run_inventory.csv` has **308** rows

So current derived analysis outputs are **stale** and must not be treated as authoritative until regenerated.

## Directly comparable complete slices available now

### Full-sample, immediately comparable

These slices already have both a canonical baseline and at least one compatible full-sample follow-up:

| Slice | Baseline present | Direct follow-up families now present |
| --- | --- | --- |
| `qwen3 / gpqa / off` | yes | oracle, wrong, stored |
| `qwen3 / gpqa / on` | yes | oracle, stored |
| `qwen3 / gsm8k / off` | yes | self(flattened), stored |
| `qwen3 / gsm8k / on` | yes | self(flattened), wrong(flattened) |
| `qwen3 / mmlu / off` | yes | oracle |
| `qwen3 / mmlu / on` | yes | oracle |
| `qwen25 / gpqa / off` | yes | stored |
| `qwen25 / gsm8k / off` | yes | stored |
| `qwen25 / aime / off` | yes | stored |
| `qwen25 / mmlu / off` | yes | stored |
| `llama32_3b / gpqa / off` | yes | stored |
| `llama32_3b / gsm8k / off` | yes | stored |
| `llama32_3b / aime / off` | yes | stored |
| `llama32_3b / mmlu / off` | yes | stored |
| `mistral7b / gpqa / off` | yes | stored |
| `mistral7b / gsm8k / off` | yes | stored |
| `mistral7b / aime / off` | yes | stored |
| `mistral7b / mmlu / off` | yes | stored |

### Comparable, but better treated as pilot/supporting slices

- 50-item Qwen3 protocol sweeps from 2026-03-13
- small smoke/minirun slices

These are still useful for mechanism diagnosis and for deciding which full-sample slice to close next.

## Partial-run decision

Two partial-only runs remain on disk:

1. `qwen3_1p7b_gsm8k_protocol_kfull_gsm8k_on_canonical_k4`
   - intended slice: `qwen3 / gsm8k / thinking_on / single_turn_flattened / self_history / cross_domain / k=4`
2. `qwen3_1p7b_gsm8k_gsm8k_wrong_history_cross_domain_full_k8`
   - intended slice: `qwen3 / gsm8k / thinking_on / single_turn_flattened / wrong_history / cross_domain / k=8`

### Recommendation

**Keep both lanes and explicitly finish or cleanly rerun them** rather than archive them now.

Reason:

- both belong to an already-started, claim-relevant slice,
- both help close the `qwen3 / gsm8k / thinking_on / flattened / cross_domain` provenance story,
- both are more valuable than starting brand-new lanes.

However:

- do not trust partial-only state as evidence,
- if resume fidelity is uncertain, rerun cleanly instead of inheriting ambiguous partials.
- operationally, the current recommendation is:
  - **prefer clean rerun over resume**
  - because one partial log ends with null-byte corruption and the other stopped mid-run without a normal end-of-run summary

## Minimal next experiment set after docs/results sync

Before any run:

1. refresh derived analysis from the latest scoreboard,
2. mark the two partial lanes as `keep-and-complete`,
3. freeze which slices are main-table candidates.

Then the **minimum** new execution set should be:

1. complete or rerun  
   `qwen3 / gsm8k / thinking_on / single_turn_flattened / self_history / cross_domain / k=4`
2. complete or rerun  
   `qwen3 / gsm8k / thinking_on / single_turn_flattened / wrong_history / cross_domain / k=8`
3. if a clean self-history `k` curve is required for the same slice, add  
   `qwen3 / gsm8k / thinking_on / single_turn_flattened / self_history / cross_domain / k=8`

## Experiments safe to pause now

Pause these until the main claim tables and analysis are synchronized:

- any new model family expansion beyond the currently completed multimodel set
- new parser/prompt-control rescue sweeps
- new dataset additions
- extra exploratory axes beyond the current structure/provenance/relation story
- any run whose only justification is “more coverage” rather than “closes a main-claim slice”

## Immediate operator rule

Do not ask “what else can we run?” yet.

Ask instead:

1. Which current rows belong in the main claim?
2. Which current rows are secondary?
3. Which current incomplete lanes are worth closing?
4. Which analysis files must be regenerated before any new interpretation?
