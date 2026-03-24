# ANALYSIS

- Date: 2026-03-20

## 2026-03-24 readable snapshot

Current shareable snapshot files now exist at the repo root:

- `RESULT.md`
- `result_snapshot.csv`

Current artifact counts:

- `Legacy/results/summary/scoreboard.csv`: **579** rows
- `analysis/tables/run_inventory.csv`: **579** rows

Current interpretation:

1. **Main**
   - the multimodel external-contamination slice is complete
   - average delta vs canonical single-turn baseline differs by model family:
     - `qwen25`: negative on average
     - `llama32_3b`: mildly negative on average
     - `mistral7b`: positive on average
   - so accumulated contaminated-history robustness is clearly model-sensitive

2. **Supporting**
   - Qwen3 / GPQA provenance slice is complete
   - several same-domain provenance conditions outperform the single-turn baseline
   - the strongest current row is `stored_incorrect / k=4`, which sits above the canonical baseline while sharply reducing format failures

3. **Appendix**
   - Qwen3 / GSM8K / thinking-on / flattened self-vs-wrong is now fully populated, including optional `self / k=8`
   - the strongest degradation is `self / k=8`
   - that row sits **-0.3692** below the canonical single-turn baseline, which is the clearest direct evidence that accumulated conversation history can strongly perturb final-turn accuracy

4. **Broad backfill**
   - after the appendix closure, the only remaining generated gap set was `Legacy/configs/generated/multimodel_single_turn_pools/`
   - completed from that queue so far:
     - `llama32_3b / aime / single_turn_pool / off`
     - `mistral7b / aime / single_turn_pool / off`
     - `llama32_3b / gpqa / single_turn_pool / off`
     - `mistral7b / gpqa / single_turn_pool / off`
     - `qwen25_1p5b / aime / single_turn_pool / off`
   - GPUs `5,6,7` are still progressing on the remaining backfill lanes

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

- at that earlier point, `Legacy/results/summary/scoreboard.csv` had moved ahead of the derived tables,
- that stale-state mismatch has since been repaired.

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

- `analysis/tables/run_inventory.csv` refreshed to **579** rows
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

## 2026-03-24 execution extension

After the appendix branch was fully closed, the next broad generated gap set was identified:

- `Legacy/configs/generated/multimodel_single_turn_pools/`

Status at the latest refresh:

- `qwen3_core_paper`: **256 / 256 complete**
- `multimodel_pool_followups`: **264 / 264 complete**
- `multimodel_single_turn_pools`: the only remaining generated gap set
  - total configs: **12**
  - families covered: `llama32_3b`, `mistral7b`, `qwen25_1p5b`
  - datasets covered: `aime`, `gpqa`, `gsm8k`, `mmlu`

An unattended queue was launched on GPUs `2,5,6,7` with a 10-second gap between jobs.

Completed from that queue so far:

- `run-20260324T050441Z-a02c523e`
  - `llama32_3b / aime / single_turn / k=0 / same_domain`
- `run-20260324T051159Z-3a804857`
  - `mistral7b / aime / single_turn / k=0 / same_domain`
- `run-20260324T051316Z-a0f54d2b`
  - `llama32_3b / gpqa / single_turn / k=0 / same_domain`
- `run-20260324T051809Z-47f05ae6`
  - `mistral7b / gpqa / single_turn / k=0 / same_domain`
- `run-20260324T051905Z-681c31be`
  - `qwen25_1p5b / aime / single_turn / k=0 / same_domain`

The active queue means the repo is now in a new state:

- the frozen paper slices are already closed,
- ongoing work is baseline backfill / packaging support,
- not paper-story redefinition.
