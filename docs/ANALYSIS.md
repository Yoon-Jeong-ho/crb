# ANALYSIS

- Date: 2026-03-20

## Current top-line conclusion

CRB should now be interpreted first as a **protocol-definition problem**, not as an open-ended run-generation problem.

The current paper-facing claim is:

> standard single-turn benchmark accuracy does not fully characterize robustness under accumulated conversational history, and CRB provides a target-only protocol for measuring that missing robustness axis.

## What changed since the 2026-03-11 continuation notes

The repo has moved past the original GPQA/Qwen3 parserfix-focused continuation state.

Between 2026-03-16 and 2026-03-18, the on-disk artifact state expanded to include:

- single-turn full-sample baselines for multiple datasets and multiple model families,
- `stored_history` follow-up workflows,
- multimodel pool-backed comparison runs,
- relation controls including `same_domain_other_dataset`.

At the same time, the docs and derived analysis outputs did **not** fully keep up:

- `Legacy/results/summary/scoreboard.csv` now has **573** rows,
- `analysis/tables/run_inventory.csv` still has **308** rows.

So the immediate task is not “run more”; it is “restate the claim, baseline, and evidence classes correctly.”

## Claim freeze

Use the following interpretation as the current main story:

1. **Baseline**
   - `single_turn`, `k=0`, no dummy history
2. **Headline phenomenon**
   - final-target accuracy can change under accumulated history even when the target item is unchanged
3. **Main decomposition axes**
   - structure: `multi_turn` vs `single_turn_flattened`
   - provenance: `self`, `oracle`, `wrong`, `stored`
   - relation: same-benchmark / `same_domain_other_dataset` / `cross_domain`
   - history size: `k`

## Story layout freeze

### Main figure / main story

- **multimodel / stored_history / external contamination**

### Main supporting analysis

- **Qwen3 / GPQA / multi_turn / oracle-wrong-stored provenance**

### Appendix / exploratory branch

- **Qwen3 / GSM8K / thinking-on / flattened / self-vs-wrong**

## Important interpretation freeze for `stored_history`

`stored_history` should not be described as if it were just a cheaper `self_history`.

The right interpretation is:

- `self_history` = self-contamination / self-accumulation
- `stored_history` = externally injected contaminated-history robustness

That distinction makes the recent multimodel results much more useful: they are not a detour away from CRB, they are evidence for the **external contamination** branch of the protocol.

## What evidence is strongest right now

### Strongest directly usable evidence

1. **Full-sample single-turn baselines**
   - Qwen3 off/on across `gpqa`, `gsm8k`, `aime`, `mmlu`
   - Qwen2.5 / Llama-3.2-3B / Mistral-7B off across the same benchmark set

2. **Full-sample Qwen3 provenance slices**
   - `qwen3/gpqa` with `oracle`, `wrong`, and `stored` follow-ups
   - `qwen3/gsm8k` with flattened `self_history` and `wrong_history` follow-ups
   - `qwen3/mmlu` full-sample oracle follow-ups

3. **Full-sample multimodel stored-history slices**
   - `qwen25`, `llama32_3b`, and `mistral7b`
   - full-sample baselines plus `stored_history` follow-ups
   - usable for the generalization story of external contaminated-history robustness

### Useful but secondary evidence

- Qwen3 parserfix / strict-final / constrained-decoding / `/no_think + prefill` rescue experiments
- 50-item pilot sweeps
- smoke validation and workflow/tooling checks

These still matter, but they should not define the headline contribution.

## What not to over-claim yet

1. **Do not over-claim monotonic degradation.**
   - Several slices are non-monotonic.
   - Some stored-history conditions even outperform their single-turn baseline.
   - That is not a failure of CRB; it means the protocol is revealing a more complex robustness landscape than “more history always hurts.”

2. **Do not collapse `stored_history` into `self_history`.**
   - They answer related but different questions.

3. **Do not treat stale derived analysis as authoritative.**
   - Refresh the analysis files first.

## Current judgment on the two stranded partial runs

The two partial-only GSM8K thinking-on runs should currently be treated as:

- **keep-and-complete**, not “main-table evidence,” and not “random leftovers”

Reason:

- both close an already-started claim-relevant Qwen3/GSM8K/thinking-on/provenance slice,
- both are more valuable than opening brand-new branches,
- both fit the current protocol story.

If resume fidelity is questionable, rerun them cleanly rather than inheriting ambiguous partial state.

Current recommended operational choice:

- **clean rerun > resume**

because:

1. one partial log ends abruptly with null-byte corruption,
2. neither partial lane reached a normal completion summary,
3. these runs belong to an exploratory appendix branch, so clarity is more valuable than saving partial progress.

## Immediate analysis-first next step

The next correct move is:

1. freeze the claim and baseline,
2. refresh scoreboard-derived analysis,
3. label each run family as main / secondary / parked,
4. only then decide which minimal runs to complete.

The next mistake would be:

- widening scope again before the existing evidence is reclassified.

## 2026-03-20 execution update

The analysis-refresh phase is now complete.

### Completed analysis outputs

- `analysis/tables/run_inventory.csv` refreshed to **573** rows
- `analysis/tables/summary_table.csv` / `.md` refreshed
- `analysis/error_buckets/error_buckets.csv` / `.md` refreshed
- `analysis/figures/metric_plot.md` refreshed
- claim-specific slice tables generated:
  - `analysis/tables/main_multimodel_external_contamination.csv`
  - `analysis/tables/supporting_qwen3_gpqa_provenance.csv`
  - `analysis/tables/appendix_qwen3_gsm8k_self_vs_wrong.csv`
- figure-readiness memo written:
  - `analysis/notes/figure_ready_20260320.md`

### Figure readiness verdict

- **Main figure: ready**
  - multimodel external-contamination slice is fully populated
  - baseline join passed for all required rows
- **Supporting figure: ready**
  - Qwen3 GPQA provenance slice is fully populated
  - baseline join passed for all required rows
- **Appendix figure: ready**
  - required cells were closed on 2026-03-23:
    - `qwen3 / gsm8k / on / single_turn_flattened / self_history / cross_domain / k=4`
    - `qwen3 / gsm8k / on / single_turn_flattened / wrong_history / cross_domain / k=8`
  - optional `self_history / k=8` cell was also closed on 2026-03-24

## 2026-03-23 appendix closure update

The appendix closure work is now complete.

### Runtime fix

The prior blocker was an environment-level CUDA library resolution issue, not CRB logic:

- inherited `LD_LIBRARY_PATH=/usr/local/cuda/lib64:...` overrode the torch wheel's bundled CUDA libraries
- clean launches had to use:
  - `env -u LD_LIBRARY_PATH`
  - `PYTHONNOUSERSITE=1`

### Successful reruns

1. `wrong_history / k=8`
   - run id: `run-20260323T120127Z-b3c43227`
   - accuracy: `0.33965125094768767`
   - format failure rate: `0.02577710386656558`
2. `self_history / k=4`
   - run id: `run-20260323T143713Z-85b1af5d`
   - accuracy: `0.3639120545868082`
   - format failure rate: `0.07733131159969674`
3. `self_history / k=8` (optional lane, later closed)
   - run id: `run-20260324T044142Z-1e65b909`
   - accuracy: `0.310841546626232`
   - format failure rate: `0.04169825625473844`

The `self_history / k=4` rerun was finalized from the current clean partial state after the clean run proved healthy; the completion path used only same-config current-session partials plus same-config shard workers on GPUs `0,1,2,5,6,7`, and did **not** reuse archived partials from older hashes.

## Current operational conclusion

- main and supporting are ready for figure/table drafting now
- appendix is now also ready for figure/table drafting
- appendix optional self-history extension is now also present, so there are no remaining appendix-side rerun gaps
