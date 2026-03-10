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
- Phase: post-smoke / mini-run transition
- Status: core new paths validated, direct off/on pairs established on two benchmarks, selective sweep execution still pending

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
1. GPQA thinking-on parser/postprocessing hardening
2. selective sweep subset launch from generated configs
3. broader mini-run coverage for direct comparison conditions

## Next execution batches
### Batch 1: parser + pair hardening
- GPQA thinking-on parser/postprocessing fallback
- optional GPQA thinking-on rerun after parser change

### Batch 2: selective sweep subset
- GPQA thinking-off across `k={0,2,4,8}`
- same vs cross where feasible
- one self-history/oracle-history continuation branch

### Batch 3: benchmark pair scaling
- GSM8K off/on mini expansion
- AIME follow-up if ambiguity handling improves

## Completion heuristics
We can start treating the repository as paper-usable when:
- at least one direct off/on pair is available on two benchmarks  ✅
- at least one multi-turn vs flattened pair is available on two benchmarks  ⏳
- at least one k sweep subset is populated with real runs  ⏳
- scoreboard and analysis docs remain synchronized with results  ✅

## Current completion estimate
- infrastructure readiness: high
- smoke validation: high
- mini-run progression: medium
- sweep coverage: low-to-medium
- paper-usable analysis artifacts: medium
