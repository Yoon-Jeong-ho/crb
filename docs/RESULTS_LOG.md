# RESULTS LOG

- Date: 2026-03-11

## New runs this cycle
- 2026-03-11 — Prepared the runnable Legacy smoke path from `Legacy/` using `PYTHONPATH=src` and `/data_x/aa007878/projects/crb/.conda/envs/crb/bin/python`.
- 2026-03-11 — Re-checking the existing GPQA thinking-off smoke config returned the cached completed run `run-20260310T153733Z-9c2df9c4` because that config keeps `runtime.skip_completed: true`.
- 2026-03-11 — A fresh GPQA thinking-off smoke retry initially failed in the sandbox because `datasets.load_dataset("Idavidrein/gpqa")` could not reach the Hugging Face Hub.
- 2026-03-11 — Escalated rerun succeeded on GPU 4:
  - config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_gpu4_smoke_20260311.yaml`
  - run id: `run-20260311T053304Z-f40cce6c`
  - accuracy: `0.5`
  - format failure: `0.0`
  - json: `Legacy/results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_gpu4_smoke_20260311__f40cce6cd46fde00/run-20260311T053304Z-f40cce6c.json`
- 2026-03-11 — A fresh local-fixture fallback smoke succeeded: `mock_mmlu_multiturn_oracle_worker4_20260311` → `run-20260311T053039Z-46d4ee1f` with accuracy `0.5` and format failure rate `0.0`; a new scoreboard row was appended under `Legacy/results/summary/scoreboard.csv`.
- 2026-03-11 — Worker-5 completed a second fresh GPQA smoke on GPU 4:
  - config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_gpu4_worker5_smoke_20260311.yaml`
  - run id: `run-20260311T054045Z-c4316b30`
  - accuracy: `0.5`
  - format failure: `0.0`
  - json: `Legacy/results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_gpu4_worker5_smoke_20260311__c4316b30556d7ecf/run-20260311T054045Z-c4316b30.json`

## Legacy evidence present
- Existing historical logs/configs are present under `Legacy/logs/` and `Legacy/configs/`.
- Those runs are not yet re-certified as the active root workflow for this cycle.

## Next expected entries
1. GPQA or GSM8K + Qwen3 thinking on smoke
2. AIME numeric smoke
3. One allowed multi-GPU verification on `4,5`
