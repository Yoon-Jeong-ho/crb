# CRB Next TODO

## Highest priority
1. Add a short error-breakdown note for GPQA / GSM8K / AIME / MMLU full rows
2. Decide whether the headline narrative is “mixed benchmark sensitivity” or “GSM8K/MMLU thinking-on gains with GPQA parity and AIME failure”
3. Sync root-level docs with the completed four-benchmark table

## Medium priority
1. Launch the first selective `k={0,2,4,8}` subset from `configs/generated/qwen3_core_paper/`
2. Use GPQA thinking-off and GSM8K thinking-on as the first broader-sweep anchor lanes
3. Revisit AIME thinking-on only if we need broader full-benchmark off/on coverage

## Lower priority
1. Add richer table/figure-ready exports beyond `main_table_qwen3.csv`
2. Generate k-sweep summaries automatically from the scoreboard
3. Sync root-level docs with the new full-sample core-table state

## Current best next batch
- expand from the completed four-benchmark table into selective k-sweeps
- prioritize GPQA thinking-off and GSM8K/MMLU thinking-on as anchor lanes
- then add richer analysis artifacts

## Risks to track
- AIME thinking-on remains highly format-unstable
- GPQA thinking-on is rescued but still not superior to thinking off
- strong MMLU/GSM8K thinking-on results should not be over-generalized across all benchmarks
