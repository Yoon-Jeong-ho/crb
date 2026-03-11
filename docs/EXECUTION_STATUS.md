# EXECUTION STATUS

- Date: 2026-03-11
- Team: `crb-gpu567-continuation-gpus-5`
- Basis docs: `README.md`, `CRB_EXPERIMENT_SETUP.md`, `docs/RESULTS_LOG.md`, `docs/ANALYSIS.md`, `docs/TODO_NEXT.md`
- Env: `/data_x/aa007878/projects/crb/.conda/envs/crb`
- GPU rule for **this continuation run**: `5,6,7` only

## Current state

- [x] Root vs `Legacy/` runnable split re-confirmed
- [x] Docs refreshed for the GPU567 continuation pass
- [x] Earlier pushed baseline commits recorded: `28e4058`, `02fa431`
- [x] Historical GPQA thinking-off GPU4 smoke evidence carried forward as reference
- [x] Parserfix branch validated with a fresh GPU5 run
- [x] First true continuation-cycle result logged
- [x] One allowed multi-GPU verification completed on GPUs `5,6`
- [ ] Parserfix follow-up rerun on GPU6/7 not yet logged
- [ ] Remaining invalid outputs not yet analyzed

## Fresh verified result

- experiment: GPQA / Qwen3 thinking-on / parserfix smoke
- GPU: `5`
- config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix.yaml`
- run id: `run-20260311T060823Z-1947f5cf`
- metrics:
  - accuracy `0.375`
  - format failure `0.500`
  - parsed `4/8`
  - invalid `4/8`
- evidence:
  - JSON: `Legacy/results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix__1947f5cf9df42ec1/run-20260311T060823Z-1947f5cf.json`
  - log: `Legacy/logs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix__1947f5cf9df42ec1.log`
  - scoreboard append confirmed in `Legacy/results/summary/scoreboard.csv`

## Fresh multi-GPU verification

- experiment: GPQA / Qwen3 thinking-off / multi-GPU smoke
- GPUs: `5,6`
- config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_multigpu_gpu56_smoke_20260311.yaml`
- run id: `run-20260311T061434Z-10e36149`
- metrics:
  - accuracy `0.500`
  - format failure `0.000`
  - parsed `2/2`
  - invalid `0/2`
- evidence:
  - JSON: `Legacy/results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_multigpu_gpu56_smoke_20260311__10e361496f9e67c7/run-20260311T061434Z-10e36149.json`
  - scoreboard row: `Legacy/results/summary/scoreboard.csv`

## Active local WIP

- parserfix files currently present locally:
  - `Legacy/src/crb/evaluation/parsers.py`
  - `Legacy/tests/test_parsers.py`
  - `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix.yaml`
- meaning: the branch now has **one verified GPU5 smoke**, but it is still local/unpushed and still has `invalid_count = 4`.

## Immediate queue

1. Inspect the 4 invalid outputs from `run-20260311T060823Z-1947f5cf`.
2. Confirm whether those invalids are parse bugs or no-final-answer / truncation failures.
3. Run one follow-up parserfix smoke on GPU 6 or 7.
4. Reflect any new evidence in `docs/RESULTS_LOG.md` and `docs/ANALYSIS.md` immediately.

## Risks / blockers

- parserfix is no longer unverified, but format failure is still `0.5`.
- GPU4 smoke evidence remains helpful baseline material, not the scheduler rule for this continuation pass.
- Root package/layout mismatch still exists; docs are aligned first, code/package cleanup remains separate work.
