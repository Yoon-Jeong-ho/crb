# CRB Execution Status

_Last updated: 2026-03-11_

## Current environment
- Project root: `/data_x/aa007878/projects/crb`
- Execution env: `/data_x/aa007878/projects/crb/.conda/envs/crb`
- Python: `3.10.19`
- torch: `2.9.0+cu128`
- transformers: `4.57.6`
- vllm: `0.11.2`
- datasets: `2.21.0`
- Branch: `main`
- Recent commits before this execution cycle:
  - `e6db683` add gpqa aime and qwen3 thinking sweep support
  - `5a986c3` validate local conda env and gpu-backed vllm runs
  - `0cbe61e` build config-driven CRB evaluation pipeline scaffold

## GPU availability
- Policy GPUs: `6,7` only
- Check command:
  - `nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader`
- Snapshot at run start:
  - GPU 6: `4 MiB / 49140 MiB`, util `0%`
  - GPU 7: `4 MiB / 49140 MiB`, util `0%`
- Decision:
  - Smoke runs were safe to start on `CUDA_VISIBLE_DEVICES=6`
  - Multi-GPU expansion can wait until after smoke validation / analysis

## Ready configs
- `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off.yaml`
- `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on.yaml`
- `configs/qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_off.yaml`
- `configs/qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_on.yaml`
- `configs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off.yaml`

## Existing result state
- Scoreboard: `results/summary/scoreboard.csv`
- Existing validated older real runs:
  - `qwen25_1p5b_mmlu_multiturn_oracle_k2`
  - `qwen25_1p5b_gsm8k_flattened_self_k2`
- New runs completed in this cycle:
  - Qwen3 thinking off + GPQA
  - Qwen3 thinking on + GPQA
  - Qwen3 thinking off + AIME

## Completed runs this cycle
1. `qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off`
   - status: success
   - GPU: `6`
   - result: accuracy `0.500`, format failure `0.000`
2. `qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on`
   - status: success
   - GPU: `6`
   - result: accuracy `0.125`, format failure `0.875`
3. `qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off`
   - status: success after one config fix
   - GPU: `6`
   - result: accuracy `0.125`, format failure `0.250`

## Risks / blockers
- Qwen3 thinking-on on GPQA currently shows severe format instability (`7/8` parse failures in this smoke run).
- AIME numeric parsing is working end-to-end, but two items still fail with `ambiguous_numeric_answer` because the model emits multiple candidate numerics.
- The first AIME run failed before generation because the smoke config lacked enough cross-domain dummy candidates for manifest construction; the config was corrected by adding GPQA and MMLU dummy sources.
- Current results are still smoke-scale (`num_samples=8`), so all observations remain preliminary.

## Pending runs
1. Qwen3 thinking on + GSM8K to check whether the format-collapse is GPQA-specific
2. AIME rerun with prompt / parser adjustments if needed
3. GPQA / AIME mini runs with larger `num_samples`
4. Multi-GPU Qwen3 validation on `CUDA_VISIBLE_DEVICES=6,7`
5. Materialize paper sweep configs and queue next batch
