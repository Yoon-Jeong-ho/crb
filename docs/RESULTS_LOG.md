# RESULTS LOG

- Date: 2026-03-24

## Current meaning of this file

This file is now a **current results index**, not the full historical legacy run diary.

For historical 2026-03 legacy-only continuation logs, see:

- `docs/legacy/RESULTS_LOG_20260311.md`
- other dated files under `docs/legacy/`

## Verified CRB v2 smoke result

- config:
  - `configs_v2/pilot/mock_fixture_smoke.yaml`
- result root:
  - `results_v2/mock_fixture_smoke__1717ebb2a46d6bc6/`
- key outputs:
  - `pipeline_result.json`
  - `aggregate/summary_rows.csv`
  - `aggregate/summary.md`

## Active CRB v2 pilot

- config:
  - `configs_v2/pilot/two_models_two_benchmarks.yaml`
- launcher:
  - `scripts_v2/run_gpu2_pilot.sh`
- tmux:
  - `crb_v2_gpu2_pilot`
- live log:
  - `logs/crb_v2_gpu2_pilot_latest.log`

## Legacy reference

Legacy paper-slice artifacts still live under:

- `Legacy/results/`
- `Legacy/logs/`

but they are no longer the default execution surface for new runs.
