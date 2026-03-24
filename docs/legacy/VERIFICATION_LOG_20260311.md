# VERIFICATION LOG

- Date: 2026-03-11

## Preflight
- [x] `git status --short --branch` → `## main...origin/main` with untracked `docs/`
- [x] `tmux -V` → `tmux 3.2a`
- [x] `command -v omx` → `/mnt/raid6/aa007878/.npm-global/bin/omx`
- [x] Team pane control verified via escalated `tmux list-windows` / `tmux list-panes` (`crb-team-bootstrap-v3` window present with 7 panes)

## Code-ready
- [x] `pyproject.toml` exposes `crb-eval`, `crb-pack`, `crb-batch`, `crb-materialize`
- [x] Active CRB entrypoint verified via `./.conda/envs/crb/bin/python -c 'import crb, crb.cli.run_eval'` → `/data_x/aa007878/projects/crb/src/crb/cli/run_eval.py`
- [x] Root `src/`, `tests/`, `configs/` resolve through symlinks into `Legacy/`
- [x] `./.conda/envs/crb/bin/python -m compileall src` → pass
- [x] `PYTHONPATH=Legacy/src ./.conda/envs/crb/bin/python -m compileall Legacy/src` → pass
- [x] `./.conda/envs/crb/bin/python -m pytest tests -q` → `9 passed in 1.69s`
- [x] `PYTHONPATH=Legacy/src ./.conda/envs/crb/bin/python -m pytest Legacy/tests -q` → `9 passed in 1.86s`
- [x] Mock end-to-end path verified via `./.conda/envs/crb/bin/python -m pytest tests/test_pipeline_mock.py -q` → `1 passed in 4.31s`
- [x] Parser tests after fallback patch: `PYTHONPATH=src ../.conda/envs/crb/bin/python -m pytest tests/test_parsers.py -q` (from `Legacy/`) → `3 passed`

## Smoke-ready
- [x] Generated root smoke config exists: `configs/generated/qwen3_core_paper/qwen3_gpqa__qwen3_thinking_off__evaluation_mode-multi_turn__history_mode-oracle_history__dummy_type-same_domain__k-2.yaml`
- [x] Real GPU4 smoke config exists: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_gpu4_smoke_20260311.yaml`
- [x] Real GPU4 smoke manifest exists: `Legacy/results/manifests/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_gpu4_smoke_20260311__manifest__280958988d2e6bca.json`
- [x] Real GPU4 smoke run JSON exists: `Legacy/results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_gpu4_smoke_20260311__f40cce6cd46fde00/run-20260311T053304Z-f40cce6c.json`
- [x] GPU5 thinking-on parserfix smoke replayed successfully outside the sandbox
- [x] GPU5,6 multi-GPU GPQA smoke replayed successfully outside the sandbox
- [x] GPU7 AIME offline smoke replayed successfully outside the sandbox

## Run-verified
- [x] Real GPQA smoke artifact set verified on disk for `run-20260311T053304Z-f40cce6c`
- [x] Parsed run metrics from JSON: `dataset=gpqa`, `accuracy=0.5`, `format_failure_rate=0.0`, `parsed_count=2`, `invalid_count=0`
- [x] Scoreboard append verified via `Legacy/results/summary/scoreboard.csv` for `run-20260311T053304Z-f40cce6c`
- [x] Additional later GPQA smoke artifact also exists: `run-20260311T054045Z-c4316b30`
- [x] GPQA thinking-on parserfix smoke artifact exists: `run-20260311T060823Z-1947f5cf`
- [x] Allowed-set multi-GPU smoke artifact exists: `run-20260311T061434Z-10e36149`
- [x] GPQA thinking-on GPU6 strictfinal follow-up exists: `run-20260311T063838Z-7956de92`
- [x] AIME GPU7 offline smoke exists: `run-20260311T064335Z-1ab1abe2`

## Sandbox vs escalated path
- Sandbox-limited verification: direct tmux inspection failed inside the sandbox with `error connecting to /tmp/tmux-2057/default (Operation not permitted)` until escalated.
- Documented sandbox run failure exists in `docs/ANALYSIS.md` / `docs/RESULTS_LOG.md` (HF access issue), but this worker did **not** replay that failure.
- Escalated-success path is confirmed by the on-disk 2026-03-11 GPQA GPU4 smoke artifacts (`config`, `manifest`, `run JSON`, `scoreboard row`) for `run-20260311T053304Z-f40cce6c`.

## Verification protocol evidence
- PASS — typecheck-equivalent: `./.conda/envs/crb/bin/python -m compileall src` and `PYTHONPATH=Legacy/src ./.conda/envs/crb/bin/python -m compileall Legacy/src`
- PASS — full tests: `./.conda/envs/crb/bin/python -m pytest tests -q` → `8 passed in 3.69s`
- PASS — legacy tests: `PYTHONPATH=Legacy/src ./.conda/envs/crb/bin/python -m pytest Legacy/tests -q` → `9 passed in 1.86s`
- PASS — end-to-end mock path: `./.conda/envs/crb/bin/python -m pytest tests/test_pipeline_mock.py -q` → `1 passed in 4.31s`
- FAIL — modified-file lint: `markdownlint docs/VERIFICATION_LOG.md` / `mdl docs/VERIFICATION_LOG.md` unavailable (`no markdown linter configured`)
- PASS — regression spot-check: `PYTHONPATH=Legacy/src ./.conda/envs/crb/bin/python -m pytest Legacy/tests/test_pipeline_mock.py -q` → `1 passed in 5.53s`

## Not yet verified
- Markdown linting could not run because no markdown linter is configured.
- `README.md` packaging/doc cleanup is still incomplete even though smoke artifacts now exist.
