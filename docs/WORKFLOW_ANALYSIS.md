# Workflow + Analysis Map

This document explains how to navigate the CRB workspace **without mixing legacy and v2 execution lanes**.

## What lives where

### `src/crb_v2/` + `configs_v2/`
Use this lane for **new CRB execution**:
- baseline
- pool building
- multi-turn k-sweep
- aggregate summaries

### `Legacy/`
Use this lane for:
- historical result comparison
- legacy parser/scorer behavior reference
- paper-slice archaeology on old artifacts

Do not use it as the default launcher for new work.

### `docs/`
Use this folder for current operator-facing state:
- `CRB_EXPERIMENT_SETUP.md`
- `docs/EXECUTION_STATUS.md`
- `docs/RESULTS_LOG.md`
- `docs/ANALYSIS.md`
- `docs/TODO_NEXT.md`
- `docs/crb_v2/README.md`

### `docs/legacy/`
Use this folder only when you need dated historical notes that no longer describe the current runtime.

### `analysis/`
Use this folder for derived outputs from artifact sets.
Some current files are still legacy-scoreboard oriented, so treat them as legacy analysis until a v2 analysis pass is added.

## Recommended reading / working order

1. `README.md`
2. `docs/crb_v2/README.md`
3. `CRB_EXPERIMENT_SETUP.md`
4. `docs/EXECUTION_STATUS.md`
5. `docs/TODO_NEXT.md`
6. `docs/RESULTS_LOG.md`
7. `docs/ANALYSIS.md`
8. `docs/crb_v2/BENCHMARKS_AND_SCORING.md`
9. `docs/crb_v2/FAILURE_TAXONOMY.md`
10. `docs/crb_v2/EXPERIMENT_MATRIX.md`
11. `analysis/README.md`
12. `Legacy/README.md` only if you need legacy reference behavior

## Current execution loop

1. run `crb_v2` from config
2. inspect `results_v2/<experiment>__<hash>/`
3. verify baseline / pool / sweep / aggregate outputs
4. update docs with verified conclusions
5. only then widen runtime scope

## Current analysis loop

1. separate v2 outputs from legacy outputs
2. do not merge them casually into one summary unless the comparison is explicit
3. for legacy scoreboard analysis, continue using `tools/`
4. for v2 run analysis, prefer the aggregate CSV/MD under `results_v2/.../aggregate/`
5. write conclusions back into `docs/ANALYSIS.md` or `docs/TODO_NEXT.md`
