# Workflow + Analysis Map

This document explains how to navigate the CRB workspace **without launching new experiments**.

## What lives where

### `research/`
Use this folder for:
- benchmark/background papers
- CRB claim framing
- related-work positioning
- analysis questions worth answering next
- methodology extension ideas before new runs are scheduled

Useful starting files:
- `research/README.md`
- `research/directions.md`
- `research/related_work_buckets.md`
- `research/methodology_extensions.md`

### `docs/`
Use this folder for the operator-facing state of the project:
- `docs/EXECUTION_STATUS.md` — what has been verified
- `docs/RESULTS_LOG.md` — run-by-run evidence log
- `docs/ANALYSIS.md` — current interpretation of the evidence
- `docs/TODO_NEXT.md` — next decisions / next actions
- `docs/WORKFLOW_ANALYSIS.md` — this navigation guide

### `analysis/`
Use this folder for derived outputs from existing artifacts:
- `analysis/README.md` — analysis lane overview
- `analysis/tables/` — run inventory and grouped tables
- `analysis/error_buckets/` — invalid-output/error taxonomy outputs
- `analysis/figures/` — Mermaid plots and figure-ready summaries
- `analysis/notes/` — short memos before they are promoted into `docs/`

### `docs/analysis/`
Use this subfolder for operator-facing analysis notes:
- `docs/analysis/README.md` — analysis lane overview
- `docs/analysis/analysis_methods.md` — concrete aggregation/comparison methods
- `docs/analysis/analysis_types.md` — which analysis package to produce for which goal
- `docs/analysis/methodology_extensions.md` — follow-up protocol extensions worth considering later
- `docs/analysis/operator_checklist.md` — concise next-step checklist for the next operator

### `tools/`
Use this lane for lightweight, read-only summaries over existing `Legacy/` artifacts:
- `python -m tools.aggregate_results`
- `python -m tools.build_tables`
- `python -m tools.bucket_errors`
- `python -m tools.plot_results`
- `tools/README.md` — script usage and output conventions

These scripts should read from `Legacy/results/` and `Legacy/logs/`; they should not launch new runs or rewrite raw artifacts.

### `Legacy/`
`Legacy/` is still the canonical runnable CRB tree:
- code: `Legacy/src/`
- configs: `Legacy/configs/`
- tests: `Legacy/tests/`
- raw results: `Legacy/results/`
- raw logs: `Legacy/logs/`

If you are reading execution evidence, prefer `Legacy/results/` and `Legacy/logs/` over the root `results/` / `logs/` paths.

## Recommended reading / working order

1. `README.md`
2. `CRB_EXPERIMENT_SETUP.md`
3. `docs/WORKFLOW_ANALYSIS.md`
4. `docs/EXECUTION_STATUS.md`
5. `docs/RESULTS_LOG.md`
6. `docs/ANALYSIS.md`
7. `docs/TODO_NEXT.md`
8. `research/README.md`
9. `research/directions.md`
10. `research/related_work_buckets.md`
11. `research/methodology_extensions.md`
12. `docs/analysis/README.md` and the specific analysis note you need
13. `tools/README.md` and the matching tool script if you need a repeatable summary
14. matching raw files in `Legacy/results/` and `Legacy/logs/`

## Analysis loop

1. Read the current decision state in `docs/`.
2. Choose the smallest useful analysis package from `docs/analysis/`.
3. Pull the matching raw evidence from `Legacy/results/` and `Legacy/logs/`.
4. If the comparison should be repeatable, use the relevant `tools/` module to aggregate the slice instead of hand-copying rows.
5. Compare runs across the core CRB axes:
   - `k`
   - `multi_turn` vs `flattened`
   - `self_history` vs `oracle_history`
   - `same_domain` vs `cross_domain`
   - thinking-on control variants where relevant
6. Separate:
   - accuracy changes
   - format / parse failures
   - invalid-output patterns
7. Write the conclusion back into `docs/ANALYSIS.md` or `docs/TODO_NEXT.md`.

## Current high-value operator checklist

- [ ] Compare parserfix vs strict-final vs choice-only vs `/no_think` + prefill using the already logged evidence.
- [ ] Build a compact summary view from `Legacy/results/summary/scoreboard.csv` plus the matching run JSON files.
- [ ] Refresh `analysis/tables/run_inventory.csv`, `analysis/tables/summary_table.csv`, and `analysis/error_buckets/error_buckets.csv` before writing new conclusions.
- [ ] Bucket invalid GPQA thinking-on outputs before changing parsing/prompting logic.
- [ ] Decide whether the combined constrained + `/no_think` + prefill path stays as a fallback.
- [ ] Only after the analysis pass is complete, queue the next `Legacy/` rerun or dataset extension.
