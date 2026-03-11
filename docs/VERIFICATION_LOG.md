# VERIFICATION LOG

- Date: 2026-03-11

## Preflight
- [x] `git status --short --branch` → `## main...origin/main` with untracked `docs/`
- [x] `tmux -V` → `tmux 3.2a`
- [x] `command -v omx` → `/mnt/raid6/aa007878/.npm-global/bin/omx`
- [x] Team pane control verified via `tmux list-windows` / `tmux list-panes` (`crb-team-bootstrap-v3` window present with 7 panes)
- [x] Active CRB entrypoint verified via `./.conda/envs/crb/bin/python -c 'import crb, crb.cli.run_eval'` → `/data_x/aa007878/projects/crb/src/crb/cli/run_eval.py`
- [x] Smoke config verified via `test -f configs/generated/qwen3_core_paper/qwen3_gpqa__qwen3_thinking_off__evaluation_mode-multi_turn__history_mode-oracle_history__dummy_type-same_domain__k-2.yaml`
- [x] Smoke run artifact verified via recorded run JSON `Legacy/results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_gpu4_worker5_smoke_20260311__c4316b30556d7ecf/run-20260311T054045Z-c4316b30.json`
- [x] Scoreboard append verified via `Legacy/results/summary/scoreboard.csv` (24 rows; latest observed run id `run-20260311T054045Z-c4316b30`)

## Verification protocol evidence
- PASS — typecheck-equivalent: `./.conda/envs/crb/bin/python -m compileall src` and `PYTHONPATH=Legacy/src ./.conda/envs/crb/bin/python -m compileall Legacy/src`
- PASS — full tests: `./.conda/envs/crb/bin/python -m pytest tests -q` → `8 passed in 3.69s`
- PASS — legacy tests: `PYTHONPATH=Legacy/src ./.conda/envs/crb/bin/python -m pytest Legacy/tests -q` → `8 passed in 5.57s`
- PASS — end-to-end mock path: `./.conda/envs/crb/bin/python -m pytest tests/test_pipeline_mock.py -q` → `1 passed in 4.31s`
- FAIL — modified-file lint: `markdownlint docs/VERIFICATION_LOG.md` / `mdl docs/VERIFICATION_LOG.md` unavailable (`no markdown linter configured`)
- PASS — regression spot-check: `PYTHONPATH=Legacy/src ./.conda/envs/crb/bin/python -m pytest Legacy/tests/test_pipeline_mock.py -q` → `1 passed in 5.53s`

## Notes
- Root `src/`, `tests/`, and `configs/` are available via symlinks into `Legacy/`; the earlier “root missing” assumption is stale.
- `README.md` is now a bootstrap wrapper doc, but the package/docs contract still needs cleanup.
- Fresh smoke evidence now exists from the current cycle, not only historical artifacts.
