# EXECUTION STATUS

- Date: 2026-03-24
- Status: **CRB v2 is the canonical execution surface**

## Current state

- [x] `src/crb_v2/` exists as a standalone integrated pipeline
- [x] `configs_v2/` exists for smoke / pilot / full matrix execution
- [x] `pipeline_tests/` exists and passes
- [x] `docs/crb_v2/` exists and documents benchmark mapping, failure taxonomy, and experiment matrix
- [x] `Legacy/` remains preserved as reference-only runtime history
- [x] fixture smoke run completed end-to-end
- [ ] GPU 2 real-model pilot is still running
- [ ] full matrix has not been launched yet

## Verified commands

```bash
PYTHONNOUSERSITE=1 /data_x/aa007878/projects/crb/.conda/envs/crb/bin/python -m pytest pipeline_tests -q
PYTHONNOUSERSITE=1 /data_x/aa007878/projects/crb/.conda/envs/crb/bin/python -m crb_v2.cli --config configs_v2/pilot/mock_fixture_smoke.yaml
```

## Verified outputs

Smoke result root:

- `results_v2/mock_fixture_smoke__1717ebb2a46d6bc6/`

Key artifacts:

- `results_v2/mock_fixture_smoke__1717ebb2a46d6bc6/pipeline_result.json`
- `results_v2/mock_fixture_smoke__1717ebb2a46d6bc6/aggregate/summary_rows.csv`
- `results_v2/mock_fixture_smoke__1717ebb2a46d6bc6/aggregate/summary.md`

## Active pilot

- tmux session:
  - `crb_v2_gpu2_pilot`
- launcher:
  - `scripts_v2/run_gpu2_pilot.sh`
- config:
  - `configs_v2/pilot/two_models_two_benchmarks.yaml`
- live log:
  - `logs/crb_v2_gpu2_pilot_latest.log`

Current pilot scope:

- models:
  - `qwen25_7b_instruct`
  - `llama31_8b_instruct`
- benchmarks:
  - `gsm8k`
  - `boolq`
- `k`:
  - `0, 2, 4`

## Canonical next milestone

The next milestone is not “more legacy backfill.”

It is:

1. finish GPU 2 pilot
2. verify baseline / pool / sweep / aggregate outputs
3. fix any pilot-level adapter / pool / truncation issues
4. then decide whether `configs_v2/full/full_matrix.yaml` is ready to launch

## Archived docs

Older legacy-only continuation notes were moved to `docs/legacy/`.
