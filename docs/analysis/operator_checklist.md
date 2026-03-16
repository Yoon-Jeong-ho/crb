# Operator Checklist

Use this checklist when continuing CRB analysis work without launching fresh experiments from this lane.

## Immediate

- [ ] Pick one decision slice to summarize first (for example: GPQA thinking-on control comparison).
- [ ] Pull the matching rows from `Legacy/results/summary/scoreboard.csv`.
- [ ] Copy the starter columns first: `run_id`, `dataset`, `evaluation_mode`, `history_mode`, `dummy_type`, `k`, `thinking_mode`, `num_items`, `accuracy`, `format_failure_rate`, `result_json_path`.
- [ ] Record the exact run ids and JSON paths used in the summary.
- [ ] Build one small table with accuracy, parsed count, invalid count, and format failure rate.
- [ ] Write one sentence on whether the change helped reasoning, formatting, or both.

## Next

- [ ] Run item-level paired deltas for the highest-value comparison (`baseline` vs `winner`).
- [ ] Bucket invalid outputs into a small fixed taxonomy (`no_final_answer`, `multiple_answers`, `reasoning_only`, `malformed_numeric`, `other`).
- [ ] Check whether same-domain interference is larger than cross-domain interference on the best-covered slice.
- [ ] Check whether self-history degrades more than oracle-history on the same target set.
- [ ] Only add a plot after the underlying table already supports a clear claim.

## Before promoting a conclusion

- [ ] Confirm the comparison uses the same dataset and compatible target set.
- [ ] Confirm format-failure improvements did not hide an accuracy drop.
- [ ] Confirm the result is not based on a single fragile `n=8` slice unless clearly labeled as provisional.
- [ ] Keep the main story on accumulated-history interference; keep thinking-control variants secondary.

## Handoff notes

- [ ] Save new analysis summaries under `docs/analysis/` instead of editing raw result artifacts.
- [ ] Update `docs/ANALYSIS.md` only after the supporting table/summary exists.
- [ ] If new tooling is added later, point it at `Legacy/results/` and `Legacy/logs/` as read-only sources.
