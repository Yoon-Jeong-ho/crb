# CRB Results Log

## 2026-03-10 / 2026-03-11 staged execution

### Stage 1: pre-run status check
- Checked git status / branch / recent commits.
- Verified env imports from `/data_x/aa007878/projects/crb/.conda/envs/crb`.
- Verified GPU availability for devices 6 and 7 before starting any run.
- Confirmed required Qwen3 / GPQA / AIME configs exist.
- Confirmed existing scoreboard and prior Qwen2.5 smoke results exist.

### Stage 2: GPQA / Qwen3 thinking off smoke
- Config: `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off.yaml`
- GPU: `CUDA_VISIBLE_DEVICES=6`
- Status: success
- Result JSON:
  - `results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off__3a1145ccbdfc2637/run-20260310T145435Z-3a1145cc.json`
- Metrics:
  - accuracy `0.500`
  - format_failure_rate `0.000`

### Stage 3: GPQA / Qwen3 thinking on smoke
- Config: `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on.yaml`
- GPU: `CUDA_VISIBLE_DEVICES=6`
- Status: success
- Result JSON:
  - `results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on__345dde13847d198f/run-20260310T145730Z-345dde13.json`
- Metrics:
  - accuracy `0.125`
  - format_failure_rate `0.875`
- Observation:
  - strong format collapse under GPQA thinking-on.

### Stage 4: AIME / first attempt
- Config: `configs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off.yaml`
- GPU: `CUDA_VISIBLE_DEVICES=6`
- Status: failed before generation
- Failure:
  - `ManifestError: Not enough cross_domain dummy candidates`
- Fix:
  - added GPQA and MMLU dummy sources to the AIME config.

### Stage 5: AIME / rerun after fix
- Config: `configs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off.yaml`
- GPU: `CUDA_VISIBLE_DEVICES=6`
- Status: success
- Result JSON:
  - `results/runs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off__b401cc4022eaea64/run-20260310T150040Z-b401cc40.json`
- Metrics:
  - accuracy `0.125`
  - format_failure_rate `0.250`

### Stage 6: GSM8K / Qwen3 thinking on follow-up
- Config: `configs/qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_on.yaml`
- GPU: `CUDA_VISIBLE_DEVICES=6`
- Status: success
- Result JSON:
  - `results/runs/qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_on__c56d79e297ea6e15/run-20260310T153509Z-c56d79e2.json`
- Metrics:
  - accuracy `0.125`
  - format_failure_rate `0.125`
- Observation:
  - thinking-on remains low-accuracy here, but parser stability is far better than GPQA.

### Stage 7: GPQA / multi-GPU smoke
- Config: `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_multigpu_smoke.yaml`
- GPU: `CUDA_VISIBLE_DEVICES=6,7`
- Status: success
- Result JSON:
  - `results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_multigpu_smoke__9c2df9c41af27e8f/run-20260310T153733Z-9c2df9c4.json`
- Metrics:
  - accuracy `0.500`
  - format_failure_rate `0.000`

### Stage 8: GPQA / thinking-on strict-final rescue attempt
- Config: `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_strictfinal.yaml`
- GPU: `CUDA_VISIBLE_DEVICES=6`
- Status: success
- Result JSON:
  - `results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_strictfinal__4227014d5385a505/run-20260310T154231Z-4227014d.json`
- Metrics:
  - accuracy `0.000`
  - format_failure_rate `1.000`
- Observation:
  - stricter final-answer wording alone did not help.

### Stage 9: Sweep materialization + test hygiene
- Ran: `bash scripts/materialize_qwen3_core_sweep.sh`
- Output:
  - `256` generated configs under `configs/generated/qwen3_core_paper/`
- Ran: `pytest -q`
- Result:
  - `8 passed`

### Stage 10: GSM8K / Qwen3 thinking off smoke pair completion
- Config: `configs/qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_off.yaml`
- GPU: `CUDA_VISIBLE_DEVICES=6`
- Status: success
- Result JSON:
  - `results/runs/qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_off__6e97f2ab759ca496/run-20260310T160140Z-6e97f2ab.json`
- Metrics:
  - accuracy `0.375`
  - format_failure_rate `0.250`
- Observation:
  - direct GSM8K off/on pair is now available.

### Stage 11: GPQA / Qwen3 thinking off mini run
- Config: `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_minirun.yaml`
- GPU: `CUDA_VISIBLE_DEVICES=6`
- Status: success
- Result JSON:
  - `results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_minirun__28b8ad1633d32ddb/run-20260310T160758Z-28b8ad16.json`
- Metrics:
  - accuracy `0.40625`
  - format_failure_rate `0.000`
  - `num_items=32`
- Observation:
  - GPQA thinking-off remains stable beyond smoke scale.

### Stage 12: AIME / Qwen3 thinking off mini run
- Config: `configs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off_minirun.yaml`
- GPU: `CUDA_VISIBLE_DEVICES=6`
- Status: success
- Result JSON:
  - `results/runs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off_minirun__e7fdd9b430c2034b/run-20260310T161109Z-e7fdd9b4.json`
- Metrics:
  - accuracy `0.125`
  - format_failure_rate `0.250`
  - `num_items=16`
- Observation:
  - AIME behavior is consistent with the smoke run: benchmark path is valid, ambiguity remains.

### Stage 13: Preliminary aggregate tables
- Added script: `scripts/aggregate_preliminary_results.py`
- Generated:
  - `results/analysis/latest_qwen3_runs.csv`
  - `results/analysis/latest_qwen3_runs_canonical.csv`
  - `results/analysis/direct_qwen3_pairs.csv`
  - `results/analysis/direct_qwen3_pairs.json`
  - `results/analysis/summary_overview.json`
- Current canonical direct pairs:
  - GPQA off vs on
  - GSM8K off vs on

### Current conclusion
- The project has now moved beyond pure smoke validation for GPQA thinking-off and AIME thinking-off.
- Direct Qwen3 off/on comparison pairs now exist for both GPQA and GSM8K.
- The next major bottleneck is parser/postprocessing support for GPQA thinking-on.
