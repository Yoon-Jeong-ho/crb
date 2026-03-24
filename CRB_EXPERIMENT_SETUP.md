# CRB Experiment Setup

## 0. Current continuation snapshot (2026-03-24)

- canonical new execution surface:
  - code: `src/crb_v2/`
  - configs: `configs_v2/`
  - tests: `pipeline_tests/`
  - docs: `docs/crb_v2/`
  - outputs: `results_v2/`
- preserved legacy reference surface:
  - code/config/tests/results: `Legacy/`
- env:
  - python: `/data_x/aa007878/projects/crb/.conda/envs/crb/bin/python`
- active real-model pilot lane:
  - config: `configs_v2/pilot/two_models_two_benchmarks.yaml`
  - launcher: `scripts_v2/run_gpu2_pilot.sh`
  - tmux: `crb_v2_gpu2_pilot`
  - log symlink: `logs/crb_v2_gpu2_pilot_latest.log`
- fixed smoke lane already verified:
  - config: `configs_v2/pilot/mock_fixture_smoke.yaml`
  - result root: `results_v2/mock_fixture_smoke__1717ebb2a46d6bc6/`

## 0.1 Primary rule

For all **new CRB execution work**, use `crb_v2`.

- Allowed:
  - `python -m crb_v2.cli --config configs_v2/...`
- Reference-only:
  - `Legacy/` code, configs, and old artifacts
- Disallowed default pattern:
  - reopening ad hoc one-off legacy runs as the main execution surface

## 0.2 What CRB v2 is expected to do

One config / one CLI should close the whole loop:

1. single-turn baseline
2. parseable correct / incorrect / oracle pool construction
3. relation-aware multi-turn `k` sweep
4. aggregate CSV / Markdown reporting

Current implemented stage map:

- `src/crb_v2/baseline.py`
- `src/crb_v2/pools.py`
- `src/crb_v2/sweep.py`
- `src/crb_v2/aggregate.py`
- `src/crb_v2/pipeline.py`

## 0.3 Protocol rules currently enforced in v2

- incorrect pool excludes parse / format failures
- oracle pool uses gold final answer only
- supported relations:
  - `same_benchmark`
  - `same_domain_other_benchmark`
  - `cross_domain`
- supported provenances:
  - `model_correct`
  - `model_incorrect`
  - `oracle`
- supported `k` values:
  - `0, 2, 4, 8, 16, 32`
- truncation / overflow / insufficient-pool cases are stored as reason codes

## 1. Current verified status

### 1.1 Code / tests

Verified commands:

```bash
PYTHONNOUSERSITE=1 /data_x/aa007878/projects/crb/.conda/envs/crb/bin/python -m pytest pipeline_tests -q
PYTHONNOUSERSITE=1 /data_x/aa007878/projects/crb/.conda/envs/crb/bin/python -m crb_v2.cli --config configs_v2/pilot/mock_fixture_smoke.yaml
```

Verified results:

- `pipeline_tests` → `4 passed`
- smoke outputs:
  - `results_v2/mock_fixture_smoke__1717ebb2a46d6bc6/pipeline_result.json`
  - `results_v2/mock_fixture_smoke__1717ebb2a46d6bc6/aggregate/summary_rows.csv`
  - `results_v2/mock_fixture_smoke__1717ebb2a46d6bc6/aggregate/summary.md`

### 1.2 Real-model pilot

Current pilot config:

- `configs_v2/pilot/two_models_two_benchmarks.yaml`

Current pilot scope:

- models:
  - `qwen25_7b_instruct`
  - `llama31_8b_instruct`
- benchmarks:
  - `gsm8k`
  - `boolq`
- `k`:
  - `0, 2, 4`

Execution note:

- GPU 2 pilot was started through `scripts_v2/run_gpu2_pilot.sh`
- progress should be read from:
  - `tmux capture-pane -pt crb_v2_gpu2_pilot:0 | tail -n 80`
  - `tail -n 80 logs/crb_v2_gpu2_pilot_latest.log`

## 2. Current run rules

- do not create a second competing runtime surface
- do not route new experiments back into `Legacy/` unless the task is explicitly legacy archaeology
- do not include parse / format failures in incorrect pools
- do not hand-build result tables from scattered partial artifacts
- prefer config-driven execution only

## 3. Output locations

For v2:

- `results_v2/<experiment>__<config_hash>/resolved_config.json`
- `results_v2/<experiment>__<config_hash>/baseline/...`
- `results_v2/<experiment>__<config_hash>/pools/...`
- `results_v2/<experiment>__<config_hash>/sweep/...`
- `results_v2/<experiment>__<config_hash>/aggregate/summary_rows.csv`
- `results_v2/<experiment>__<config_hash>/aggregate/summary_by_group.csv`
- `results_v2/<experiment>__<config_hash>/aggregate/summary.md`

For legacy reference only:

- `Legacy/results/...`
- `Legacy/logs/...`

## 4. Legacy note

`Legacy/` still matters for:

- old paper-slice evidence
- parser/scorer reference behavior
- historical result comparison

But it is **not** the default execution surface anymore.

Historical bootstrap / continuation notes were moved under `docs/legacy/`.
