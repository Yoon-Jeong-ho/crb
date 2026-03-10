# CRB Results Log

## 2026-03-10 / 2026-03-11 staged execution

### Stage 1: pre-run status check
- Checked git status / branch / recent commits.
- Verified env imports from `/data_x/aa007878/projects/crb/.conda/envs/crb`.
- Verified GPU availability for devices 6 and 7 before starting any run.
- Confirmed required Qwen3 / GPQA / AIME configs exist.
- Confirmed existing scoreboard and prior Qwen2.5 smoke results exist.

### Stage 2: run 1
- Config: `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off.yaml`
- GPU: `CUDA_VISIBLE_DEVICES=6`
- Status: success
- Result JSON:
  - `results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off__3a1145ccbdfc2637/run-20260310T145435Z-3a1145cc.json`
- Scoreboard: appended successfully
- Metrics:
  - accuracy `0.500`
  - format_failure_rate `0.000`
- Observation:
  - baseline thinking-off path is stable enough to parse all 8 GPQA items in this smoke run.

### Stage 3: run 2
- Config: `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on.yaml`
- GPU: `CUDA_VISIBLE_DEVICES=6`
- Status: success
- Result JSON:
  - `results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on__345dde13847d198f/run-20260310T145730Z-345dde13.json`
- Scoreboard: appended successfully
- Metrics:
  - accuracy `0.125`
  - format_failure_rate `0.875`
- Observation:
  - thinking-on causes substantial format instability on this GPQA smoke run.
  - only `1/8` items parsed cleanly.
  - raw outputs show long `<think>...</think>` traces and missing canonical final-answer formatting.

### Stage 4: run 3 (first attempt)
- Config: `configs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off.yaml`
- GPU: `CUDA_VISIBLE_DEVICES=6`
- Status: failed before generation
- Failure:
  - `ManifestError: Not enough cross_domain dummy candidates`
- Root cause:
  - smoke config only had AIME + GSM8K dummy sources, both normalized to `domain=math`, so manifest generation could not build the cross-domain pack it precomputes.
- Fix applied:
  - added GPQA and MMLU dummy sources to the AIME smoke config.

### Stage 5: run 3 (rerun after fix)
- Config: `configs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off.yaml`
- GPU: `CUDA_VISIBLE_DEVICES=6`
- Status: success after config fix
- Result JSON:
  - `results/runs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off__b401cc4022eaea64/run-20260310T150040Z-b401cc40.json`
- Scoreboard: appended successfully
- Metrics:
  - accuracy `0.125`
  - format_failure_rate `0.250`
- Observation:
  - numeric evaluator is working end-to-end.
  - `6/8` items parsed, `2/8` failed with `ambiguous_numeric_answer`.
  - model quality on these AIME smoke items is low, but the pipeline path is functioning.

### Metadata / logging validation
- Scoreboard header successfully migrated to include:
  - `model_family`
  - `thinking_mode`
- Run JSON top-level fields now include:
  - `model_family`
  - `thinking_mode`
- Per-item results now include:
  - `dummy_domains`
  - `dummy_subjects`
  - `dummy_dataset_names`
  - `history_construction_mode`

### Current conclusion
- Required smoke-scale end-to-end runs are now present for:
  - GPQA + Qwen3 thinking off
  - GPQA + Qwen3 thinking on
  - AIME numeric path
- Next priority is improving thinking-on formatting robustness and extending from smoke to mini runs.
