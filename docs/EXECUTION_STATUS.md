# EXECUTION STATUS

- Date: 2026-03-11
- Team: `crb-team-bootstrap-v3-crb-expe`
- Basis docs: `CRB_EXPERIMENT_SETUP.md`, `README.md`, `README_CRB.md`, `Legacy/README.md`
- GPU rule for this run: `4,5,6,7` only
- Env: `/data_x/aa007878/projects/crb/.conda/envs/crb`

## Current state
- [x] Repo status checked (`git status`: root currently shows new `docs/` worktree for bootstrap docs)
- [x] Basis docs read
- [x] OMX team launched
- [x] Team roles defined
- [x] Root/Legacy split detected
- [x] Active runnable path confirmed in `Legacy/`
- [x] Root `README.md` filled with current bootstrap reality
- [x] One new GPQA smoke run completed on GPU 4
- [x] Promote-vs-wrap decision made (`wrap via root bridge`)
- [ ] Root package layout aligned with runnable code
- [x] Commit created (`28e4058`)
- [x] Push completed (`origin/main`)

## Role ownership
- Data Lead — dataset scope, schema, manifest/sampling policy
- Pipeline Engineer — code/config/CLI path alignment
- Verifier / Reviewer — smoke/mini validation checklist
- Experiment Operator — GPU/run execution log
- Docs & Git Maintainer — README/setup/docs/git hygiene

## Repo snapshot
- Root now exposes a bridge to the runnable Legacy pipeline:
  - `src/crb -> ../Legacy/src/crb`
  - `configs -> Legacy/configs`
  - `scripts -> Legacy/scripts`
  - `tests -> Legacy/tests`
  - `data -> Legacy/data`
- `Legacy/` still contains the working candidate pipeline (`src/crb`, configs, tests, logs, docs).
- `README.md` now acts as a root bootstrap/wrapper doc; `README_CRB.md` remains an older overview.
- `pyproject.toml` expects root `src/` and `README.md`, so packaging/docs are currently misaligned.

## Runnable path right now
- Workdir: `Legacy/`
- Import requirement: `PYTHONPATH=src`
- Primary command shape:
  - `PYTHONNOUSERSITE=1 PYTHONPATH=src /data_x/aa007878/projects/crb/.conda/envs/crb/bin/python -m crb.cli.run_eval --config ...`
- Runtime outputs currently land under:
  - `Legacy/results/runs/`
  - `Legacy/results/manifests/`
  - `Legacy/results/summary/scoreboard.csv`
  - `Legacy/logs/`

## New smoke evidence (bootstrap cycle)
- Status: success
- Date/time: `2026-03-11T05:40:45Z`
- GPU: `4`
- Experiment: `qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_gpu4_worker5_smoke_20260311`
- Run id: `run-20260311T054045Z-c4316b30`
- Metrics:
  - accuracy `0.500`
  - format failure `0.000`
  - parsed `8/8`
- Evidence:
  - JSON: `Legacy/results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_gpu4_worker5_smoke_20260311__c4316b30556d7ecf/run-20260311T054045Z-c4316b30.json`
  - scoreboard row: `Legacy/results/summary/scoreboard.csv`
  - log: `Legacy/logs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_gpu4_worker5_smoke_20260311__c4316b30556d7ecf.log`

## Immediate queue
1. Finish remaining dataset-status cleanup for GSM8K / AIME / MMLU.
2. Align root package metadata / entrypoints with the bridge or promote path.
3. Re-validate one thinking-on condition.
4. Re-validate one allowed multi-GPU condition.
5. Decide whether to keep `README_CRB.md` as historical reference or merge it into `README.md`.

## Blockers / risks
- Root repo structure does not match `pyproject.toml`.
- Dataset-backed smoke on a cold cache may require unsandboxed network access.
- Shared root `docs/RESULTS_LOG.md` is owned by another worker, so this file carries the run evidence for now.
- Some older docs still mention GPUs `6,7`; current rule is `4,5,6,7` only.
