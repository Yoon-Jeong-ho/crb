# TODO NEXT

- Date: 2026-03-20

## Immediate freeze

- [x] Stop widening the experiment scope until the claim and protocol are explicitly restated.
- [x] Fix the canonical headline baseline as `single_turn, k=0`.
- [x] Freeze the interpretation that `stored_history` is an **external contaminated-history** condition, not a drop-in synonym for `self_history`.
- [x] Freeze the story layout:
  - main = multimodel stored_history external contamination
  - supporting = Qwen3 GPQA provenance
  - appendix = Qwen3 GSM8K thinking-on flattened self-vs-wrong

## First priority: analysis + documentation sync

- [ ] Refresh `analysis/tables/run_inventory.csv` from the latest scoreboard (`573` rows currently in `Legacy/results/summary/scoreboard.csv`)
- [ ] Refresh `analysis/tables/summary_table.csv` and `summary_table.md`
- [ ] Refresh `analysis/error_buckets/error_buckets.csv` and `error_buckets.md`
- [ ] Refresh `analysis/figures/metric_plot.md`
- [ ] Mark stale derived outputs as non-authoritative until the refresh is done

## Second priority: classify the current evidence

- [ ] Label each current run family as one of:
  - `main-claim direct`
  - `secondary / implementation`
  - `parked / excluded`
- [ ] Separate:
  - canonical baselines
  - full-sample direct comparisons
  - 50-item pilot mechanism sweeps
  - parser / prompting rescue experiments
  - incomplete partial-only lanes

## Third priority: resolve the two stranded partial runs

- [ ] Decide whether to **resume cleanly** or **rerun cleanly**:
  - `qwen3_1p7b_gsm8k_protocol_kfull_gsm8k_on_canonical_k4`
  - `qwen3_1p7b_gsm8k_gsm8k_wrong_history_cross_domain_full_k8`
- [ ] If resume fidelity is uncertain, prefer rerun over trusting partial-only state
- [ ] If either lane is explicitly dropped from the main story, archive and document that decision rather than leaving it ambiguous

## Minimal next runnable set after sync

- [ ] Complete or rerun:
  - `qwen3 / gsm8k / thinking_on / single_turn_flattened / self_history / cross_domain / k=4`
- [ ] Complete or rerun:
  - `qwen3 / gsm8k / thinking_on / single_turn_flattened / wrong_history / cross_domain / k=8`
- [ ] If a full self-history `k` curve is required for the same slice, add:
  - `qwen3 / gsm8k / thinking_on / single_turn_flattened / self_history / cross_domain / k=8`

## Explicitly safe to pause

- [ ] New model-family expansion beyond the currently completed multimodel set
- [ ] New parser/decoding rescue sweeps
- [ ] New dataset additions
- [ ] Extra exploratory axes that do not close a main-claim slice

## Operator reminder

- [ ] Ask “does this close a main-claim gap?” before asking “can we run more?”
- [ ] Do not use stale derived analysis to justify new conclusions
- [ ] Do not treat `stored_history` as a hidden rename of `self_history`
