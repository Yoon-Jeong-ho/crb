# CRB v2 Integrated Pipeline

CRB v2 is the new execution surface for conversation-accumulated robustness experiments.
`Legacy/` remains reference-only. The v2 runtime lives in `src/crb_v2/` and runs the entire flow from one config:

1. single-turn baseline
2. correct / incorrect / oracle pool construction
3. relation-aware multi-turn k-sweep
4. aggregate CSV / Markdown summaries

## Entry points

- CLI: `PYTHONNOUSERSITE=1 /data_x/aa007878/projects/crb/.conda/envs/crb/bin/python -m crb_v2.cli --config <config>`
- Console script after install: `crb-v2 --config <config>`

## Directory map

- `src/crb_v2/pipeline.py` — top-level orchestrator
- `src/crb_v2/baseline.py` — single-turn baseline execution
- `src/crb_v2/pools.py` — pool construction and prefix-consistent manifests
- `src/crb_v2/sweep.py` — multi-turn k-sweep execution
- `src/crb_v2/aggregate.py` — CSV/Markdown aggregate summaries
- `src/crb_v2/benchmarks/` — benchmark adapters, extraction, scoring
- `configs_v2/` — smoke / pilot / full-matrix configs
- `pipeline_tests/` — v2 smoke and parser tests

## Smoke test

Verified command:

```bash
PYTHONNOUSERSITE=1 /data_x/aa007878/projects/crb/.conda/envs/crb/bin/python \
  -m crb_v2.cli --config configs_v2/pilot/mock_fixture_smoke.yaml
```

Verified outputs:

- `results_v2/mock_fixture_smoke__1717ebb2a46d6bc6/pipeline_result.json`
- `results_v2/mock_fixture_smoke__1717ebb2a46d6bc6/aggregate/summary_rows.csv`
- `results_v2/mock_fixture_smoke__1717ebb2a46d6bc6/aggregate/summary.md`

## Result layout

Each run writes under `results_v2/<experiment_name>__<config_hash>/`:

- `resolved_config.json`
- `baseline/<model>/<benchmark>/`
- `pools/<model>/<benchmark>/<relation>/<provenance>.json`
- `sweep/<model>/<benchmark>/<relation>/<provenance>/<k>/`
- `aggregate/summary_rows.csv`
- `aggregate/summary_by_group.csv`
- `aggregate/summary.md`
- `pipeline_result.json`

## Policy guarantees

- incorrect pool excludes format / parse failures
- oracle pool stores gold final answer only
- k-sweeps use prefix-consistent ordered dummy ids
- context overflow / truncation / invalid generation are logged as reason codes
