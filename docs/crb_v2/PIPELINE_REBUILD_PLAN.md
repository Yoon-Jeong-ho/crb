# CRB v2 Pipeline Rebuild Plan

## Goal
Build a clean-room CRB v2 pipeline under `src/crb_v2/` that treats `Legacy/` as reference-only and closes the full execution loop from baseline to aggregation via one config/CLI entrypoint.

## Constraints
- Do not patch Legacy into the main execution path.
- Reuse only limited ideas/utilities from Legacy (parsing/scoring, dataset normalization, deterministic sampling, engine interface) and record each reuse.
- Keep malformed / parse-failed outputs out of the incorrect dummy pool.
- Record explicit reason codes for parse/format/budget/runtime failures.

## Planned package layout
- `src/crb_v2/config.py` — typed config schema + YAML loader
- `src/crb_v2/failures.py` — reason codes and outcome helpers
- `src/crb_v2/types.py` — normalized item / result / pool / aggregate schemas
- `src/crb_v2/benchmarks/` — adapter interface + benchmark registry + implementations
- `src/crb_v2/engines/` — mock + vLLM generation backends
- `src/crb_v2/prompts.py` — single-turn / multi-turn prompt rendering
- `src/crb_v2/budget.py` — token budgeting and truncation policy
- `src/crb_v2/baseline.py` — single-turn collection + pool extraction
- `src/crb_v2/pools.py` — relation/provenance candidate builders + manifests
- `src/crb_v2/sweep.py` — multi-turn k-sweep execution
- `src/crb_v2/aggregate.py` — CSV/JSON/MD summaries
- `src/crb_v2/pipeline.py` — end-to-end orchestration
- `src/crb_v2/cli.py` — single entrypoint

## Validation plan
1. Unit smoke for parsing/scoring/sampling/failure taxonomy.
2. Mock-engine smoke pipeline with small local fixture datasets.
3. GPU 2 pilot with 2 models × 2 benchmarks × k={0,2,4}.
4. After pilot verification, emit a full-matrix config/launcher for broader execution.
