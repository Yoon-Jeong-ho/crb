# PIPELINE STATUS

- Date: 2026-03-11

## Current code layout
- Root: `pyproject.toml`, `README.md` (empty), `README_CRB.md`, `CRB_EXPERIMENT_SETUP.md`
- Legacy source-of-truth pipeline:
  - `Legacy/src/crb/`
  - `Legacy/configs/`
  - `Legacy/scripts/`
  - `Legacy/tests/`
  - `Legacy/data/`
- Active root bridge (chosen bootstrap strategy = wrap, not promote/delete):
  - `src/crb -> ../Legacy/src/crb`
  - `configs -> Legacy/configs`
  - `scripts -> Legacy/scripts`
  - `tests -> Legacy/tests`
  - `data -> Legacy/data`

## Required paths to settle
- [x] `configs/`
- [x] `scripts/`
- [x] `src/crb/`
- [x] `tests/`
- [x] `results/runs/`
- [x] `results/summary/scoreboard.csv`

## Checklist
- [x] Confirm current runnable entrypoint (`PYTHONPATH=src ./.conda/envs/crb/bin/python -m crb.cli.run_eval --config configs/mock_mmlu_multiturn_oracle.yaml`)
- [x] Confirm config schema for Qwen3 thinking off/on (`pytest -q` covers `tests/test_datasets_and_metadata.py`)
- [x] Confirm parser / evaluator / sampler / runner / scoreboard modules
- [x] Decide promote-vs-wrap strategy for `Legacy/` (`wrap via root symlink bridge`)
- [x] Add/repair tests for smoke path (`pytest -q` now passes from repo root)

## Verified module map
- Config loader: `src/crb/config.py`
- CLI entrypoint: `src/crb/cli/run_eval.py`
- Parser/scorer: `src/crb/evaluation/parsers.py`, `src/crb/evaluation/scorers.py`
- Runner: `src/crb/evaluation/runner.py`
- Sampler/manifest: `src/crb/sampling/dummy_sampler.py`
- Scoreboard writer: `src/crb/io/results.py`
- Root smoke tests: `tests/test_pipeline_mock.py`, `tests/test_sampler.py`, `tests/test_datasets_and_metadata.py`, `tests/test_parsers.py`

## Verification snapshot
- `./.conda/envs/crb/bin/pytest -q` → `8 passed`
- `./.conda/envs/crb/bin/python -m compileall src tests` → pass
- `PYTHONPATH=src ./.conda/envs/crb/bin/python -m crb.cli.run_eval --config configs/mock_mmlu_multiturn_oracle.yaml` → pass (`run-20260311T053009Z-6695689d`, accuracy `0.5000`)
- Outputs now present at:
  - `results/runs/mock_mmlu_multiturn_oracle__6695689dd7067f60/run-20260311T053009Z-6695689d.json`
  - `results/summary/scoreboard.csv`

## Risks
- Root workflow now resolves through symlinks, so future refactor should replace the bridge with promoted root-owned files if long-term maintenance is required.
- `README.md` is now a bootstrap wrapper, but longer-term package/docs cleanup is still needed.
