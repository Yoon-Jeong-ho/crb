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
- [x] Parserfix follow-up rerun on GPU6 logged
- [x] Remaining invalid outputs analyzed
- [x] AIME refresh on GPU7 logged

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

## Follow-up single-GPU rerun

- experiment: GPQA / Qwen3 thinking-on / parserfix + strictfinal
- GPU: `6`
- config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix_gpu6_strictfinal_20260311.yaml`
- run id: `run-20260311T063838Z-7956de92`
- metrics:
  - accuracy `0.125`
  - format failure `0.375`
  - parsed `5/8`
  - invalid `3/8`
- interpretation:
  - format failure improved vs GPU5 parserfix run
  - accuracy got worse
  - branch is still not ready to call stable

## AIME refresh

- experiment: AIME / Qwen3 thinking-off / offline smoke
- GPU: `7`
- config: `Legacy/configs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off_gpu7_offline_smoke_20260311.yaml`
- run id: `run-20260311T064335Z-1ab1abe2`
- metrics:
  - accuracy `0.125`
  - format failure `0.250`
  - parsed `6/8`
  - invalid `2/8`

## Current parserfix branch files

- parserfix files currently present locally:
  - `Legacy/src/crb/evaluation/parsers.py`
  - `Legacy/tests/test_parsers.py`
  - `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix.yaml`
- meaning:
  - parser regex improvement itself is worth keeping
  - remaining failures are mostly no-final-answer / truncation
  - next change target is prompt/decoding, not more regex expansion

## Immediate queue

1. Choose the next prompt/decoding change rather than more parser regex.
2. Decide whether GSM8K or MMLU gets the next continuation slot.
3. Keep AIME numeric path warm with the new GPU7 offline evidence.

## Risks / blockers

- parserfix is no longer unverified, but format failure is still `0.5`.
- GPU4 smoke evidence remains helpful baseline material, not the scheduler rule for this continuation pass.
- Root package/layout mismatch still exists; docs are aligned first, code/package cleanup remains separate work.
