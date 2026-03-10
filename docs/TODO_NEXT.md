# CRB Next TODO

## Highest priority
1. Add a parser/postprocessing fallback for Qwen3 GPQA thinking-on outputs
2. Launch a first selective sweep subset from `configs/generated/qwen3_core_paper/`
3. Run one thinking-on config on `CUDA_VISIBLE_DEVICES=6,7`

## Medium priority
1. Expand the GSM8K off/on pair beyond `num_samples=8`
2. Expand GPQA thinking-off beyond `num_samples=32` if useful
3. Revisit AIME numeric ambiguity reduction
4. Add regression tests for any new GPQA thinking-on parser fallback

## Lower priority
1. Add more benchmark-result aggregate scripts for paper tables
2. Generate k-sweep summaries from scoreboard automatically
3. Add richer README links to `results/analysis/` artifacts

## Current best next batch
- GPQA thinking-on parser fallback implementation
- generated subset: GPQA thinking-off, k={0,2,4,8}, oracle_history, same/cross_domain
- generated subset: GSM8K off/on continuation

## Risks to track
- GPQA thinking-on may need generation-budget or parser changes, not just prompt changes
- AIME numeric ambiguity may continue even when formatting succeeds
- selective sweep batching is now the key operational step between mini-runs and broader paper coverage
