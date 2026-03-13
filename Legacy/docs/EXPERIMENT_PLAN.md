# CRB Experiment Plan

## Goal
Drive CRB from smoke validation to paper-usable experimental coverage using a staged loop:
1. state check
2. prioritized run
3. verification
4. analysis
5. docs update
6. git update
7. next-step selection

## Current phase
- Phase: broad protocol-sweep execution
- Status: four-benchmark main table is populated; selective/broader sweep execution is active

## Completed
- Qwen3 GPQA thinking-off smoke
- Qwen3 GPQA thinking-on smoke
- Qwen3 GPQA thinking-on strict-final rescue attempt
- Qwen3 GSM8K thinking-on smoke
- Qwen3 GSM8K thinking-off smoke
- Qwen3 AIME thinking-off smoke
- Qwen3 GPQA thinking-off multi-GPU smoke
- Qwen3 GPQA thinking-off mini run (`num_samples=32`)
- Qwen3 AIME thinking-off mini run (`num_samples=16`)
- full sweep materialization (`256` configs)
- preliminary aggregate table generation in `results/analysis/`

## In progress
1. selective / broad sweep launch from generated configs
2. `k={0,2,4,8}` accumulation-curve population
3. `mode / history / domain` contrast coverage

## Next execution batches
### Batch 1: canonical k-sweep anchors
- MMLU / GPQA / GSM8K / AIME at `k={0,2,4,8}`
- prioritize the currently strongest protocol rows first

### Batch 2: mechanism comparisons
- same vs cross where feasible
- self vs oracle where feasible
- multi_turn vs flattened where feasible

### Batch 3: secondary reasoning-mode comparisons
- read thinking on/off effects on top of the mechanism rows
- keep GPQA rescue controls as supporting machinery, not the main benchmark definition

## Completion heuristics
We can start treating the repository as paper-usable when:
- at least one direct off/on pair is available on two benchmarks  ✅
- at least one multi-turn vs flattened pair is available on two benchmarks  ⏳
- at least one k sweep subset is populated with real runs  ⏳
- self vs oracle and same vs cross rows begin to accumulate beyond isolated points  ⏳
- scoreboard and analysis docs remain synchronized with results  ✅

## Current completion estimate
- infrastructure readiness: high
- smoke validation: high
- mini-run progression: medium
- sweep coverage: low-to-medium
- paper-usable analysis artifacts: medium
