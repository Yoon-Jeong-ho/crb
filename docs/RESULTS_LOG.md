# CRB Results Log

## 2026-03-10 / 2026-03-11 staged execution

### Stage 1: pre-run status check
- Checked git status / branch / recent commits.
- Verified env imports from `/data_x/aa007878/projects/crb/.conda/envs/crb`.
- Verified GPU availability for devices 6 and 7 before starting any run.
- Confirmed required Qwen3 / GPQA / AIME configs exist.
- Confirmed existing scoreboard and prior Qwen2.5 smoke results exist.

### Stage 2: GPQA / Qwen3 thinking off
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

### Stage 3: GPQA / Qwen3 thinking on
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

### Stage 4: AIME / first attempt
- Config: `configs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off.yaml`
- GPU: `CUDA_VISIBLE_DEVICES=6`
- Status: failed before generation
- Failure:
  - `ManifestError: Not enough cross_domain dummy candidates`
- Root cause:
  - smoke config only had AIME + GSM8K dummy sources, both normalized to `domain=math`, so manifest generation could not build the cross-domain pack it precomputes.
- Fix applied:
  - added GPQA and MMLU dummy sources to the AIME smoke config.

### Stage 5: AIME / rerun after fix
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

### Stage 6: GSM8K / Qwen3 thinking on follow-up
- Config: `configs/qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_on.yaml`
- GPU: `CUDA_VISIBLE_DEVICES=6`
- Status: success
- Result JSON:
  - `results/runs/qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_on__c56d79e297ea6e15/run-20260310T153509Z-c56d79e2.json`
- Scoreboard: appended successfully
- Metrics:
  - accuracy `0.125`
  - format_failure_rate `0.125`
- Observation:
  - thinking-on remains low-accuracy on this small GSM8K smoke run, but parsing is much more stable than GPQA.
  - This suggests the GPQA thinking-on failure is not simply a global parser bug.

### Stage 7: Multi-GPU validation
- Config: `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_multigpu_smoke.yaml`
- GPU: `CUDA_VISIBLE_DEVICES=6,7`
- Status: success
- Result JSON:
  - `results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_multigpu_smoke__9c2df9c41af27e8f/run-20260310T153733Z-9c2df9c4.json`
- Scoreboard: appended successfully
- Metrics:
  - accuracy `0.500`
  - format_failure_rate `0.000`
- Observation:
  - the new Qwen3 GPQA path is now validated on both single-GPU and multi-GPU execution routes.

### Stage 8: GPQA / thinking-on strict-final prompt rescue attempt
- Config: `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_strictfinal.yaml`
- GPU: `CUDA_VISIBLE_DEVICES=6`
- Status: success
- Result JSON:
  - `results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_strictfinal__4227014d5385a505/run-20260310T154231Z-4227014d.json`
- Scoreboard: appended successfully
- Metrics:
  - accuracy `0.000`
  - format_failure_rate `1.000`
- Observation:
  - stricter final-answer wording did not rescue GPQA thinking-on behavior.
  - In this smoke run it worsened parser outcomes.

### Stage 9: Sweep preparation and test hygiene
- Ran: `bash scripts/materialize_qwen3_core_sweep.sh`
- Output:
  - generated `256` concrete configs under `configs/generated/qwen3_core_paper/`
- Ran: `pytest -q`
- Result:
  - `8 passed`
- Additional maintenance:
  - isolated the mock pipeline test so future pytest runs do not pollute the real scoreboard.

### Current conclusion
- Required smoke-scale end-to-end runs are present for:
  - GPQA + Qwen3 thinking off
  - GPQA + Qwen3 thinking on
  - GSM8K + Qwen3 thinking on
  - AIME numeric path
- Qwen3 thinking-on instability appears much worse on GPQA than on GSM8K.
- Multi-GPU Qwen3 validation is now complete for one GPQA smoke path.
