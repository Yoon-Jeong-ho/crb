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

- [x] Refresh `analysis/tables/run_inventory.csv` from the latest scoreboard (`573` rows currently in `Legacy/results/summary/scoreboard.csv`)
- [x] Refresh `analysis/tables/summary_table.csv` and `summary_table.md`
- [x] Refresh `analysis/error_buckets/error_buckets.csv` and `error_buckets.md`
- [x] Refresh `analysis/figures/metric_plot.md`
- [x] Generate claim-specific slice tables and a figure-ready memo

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

- [x] Decide whether to **resume cleanly** or **rerun cleanly**
- [x] Archive the old partial-only run dirs/logs and prefer clean rerun
- [x] Attempt the two clean appendix reruns
- [x] Fix the CUDA / torch launch blocker by using `env -u LD_LIBRARY_PATH PYTHONNOUSERSITE=1`
- [x] Close `self_history / k=4`
- [x] Close `wrong_history / k=8`

## Minimal next runnable set after sync

- [x] Optional appendix extension closed:
  - `qwen3 / gsm8k / thinking_on / single_turn_flattened / self_history / cross_domain / k=8`
- [ ] Finish the running `multimodel_single_turn_pools` backfill queue on GPUs `2,5,6,7`
  - families: `llama32_3b`, `mistral7b`, `qwen25_1p5b`
  - datasets: `aime`, `gpqa`, `gsm8k`, `mmlu`
  - completed so far: `llama32_3b/aime`, `mistral7b/aime`, `llama32_3b/gpqa`, `mistral7b/gpqa`, `qwen25_1p5b/aime`

## Explicitly safe to pause

- [ ] New model-family expansion beyond the currently completed multimodel set
- [ ] New parser/decoding rescue sweeps
- [ ] New dataset additions
- [ ] Extra exploratory axes that do not close a main-claim slice

## Operator reminder

- [ ] Ask “does this close a main-claim gap?” before asking “can we run more?”
- [ ] Do not use stale derived analysis to justify new conclusions
- [ ] Do not treat `stored_history` as a hidden rename of `self_history`
- [x] Treat main/supporting/appendix as figure-ready now; no appendix rerun gap remains
