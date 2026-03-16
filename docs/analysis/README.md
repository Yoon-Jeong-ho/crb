# Analysis Workspace

This folder turns the current CRB execution notes into a practical analysis lane.
It does **not** replace the runnable `Legacy/` tree. It organizes how to read the artifacts that already exist under `Legacy/results/` and `Legacy/logs/`.

## Folder map

- `methodology_extensions.md` — protocol extensions worth evaluating after the current baseline is stable.
- `analysis_methods.md` — concrete ways to aggregate, compare, and visualize existing result artifacts.
- `analysis_types.md` — analysis packages to produce for status reviews, operator handoffs, and paper drafting.
- `operator_checklist.md` — short next-step checklist for whoever continues the analysis work.

## Inputs to treat as read-only

- `Legacy/results/summary/scoreboard.csv`
- `Legacy/results/runs/*/*.json`
- `Legacy/logs/*.log`
- `docs/EXECUTION_STATUS.md`
- `docs/RESULTS_LOG.md`
- `docs/ANALYSIS.md`
- `research/README.md`

## Data layout notes

- `scoreboard.csv` already provides the main grouping columns: `dataset`, `evaluation_mode`, `history_mode`, `dummy_type`, `k`, `thinking_mode`, and `result_json_path`.
- Run-level JSON stores summary metrics under `metrics` and item-level rows under `per_item_results`.
- `result_json_path` values inside the scoreboard are relative paths (for example `results/runs/...`) from the runnable `Legacy/` view; resolve them against `Legacy/` when working from the repo root.

## Practical workflow

1. Freeze the slice you want to summarize (dataset, history mode, domain bucket, `k`, thinking mode).
2. Build a small result table from `scoreboard.csv` and the matching run JSON files.
3. Separate **accuracy change** from **format failure change** before drawing conclusions.
4. Inspect a small number of failures from logs/JSON to assign an error bucket.
5. Produce only the next table/plot needed for a decision; avoid speculative dashboards.

## Guardrails

- Do not launch experiments from this folder.
- Do not edit `Legacy/results/` or `Legacy/logs/` artifacts.
- Prefer compact markdown notes and small reproducible tables over large one-off reports.
