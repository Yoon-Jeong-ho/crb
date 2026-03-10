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
- Recent execution-cycle commits:
  - `f6a8976` extend qwen3 staged execution and analysis docs
  - `6709d70` run qwen3 gpqa and aime smoke validations
  - `e6db683` add gpqa aime and qwen3 thinking sweep support

## GPU availability
- Policy GPUs: `6,7` only
- Check command:
  - `nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader`
- Current interpretation:
  - GPUs 6 and 7 remain available for staged runs when checked.
  - Single-GPU smoke/mini runs continue to be the default path.
  - One multi-GPU smoke validation is complete.

## Ready configs
- `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off.yaml`
- `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_minirun.yaml`
- `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_multigpu_smoke.yaml`
- `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on.yaml`
- `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_strictfinal.yaml`
- `configs/qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_off.yaml`
- `configs/qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_on.yaml`
- `configs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off.yaml`
- `configs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off_minirun.yaml`

## Completed runs in this staged cycle
1. `qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off`
   - status: success
   - GPU: `6`
   - accuracy `0.500`, format failure `0.000`
2. `qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on`
   - status: success
   - GPU: `6`
   - accuracy `0.125`, format failure `0.875`
3. `qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off`
   - status: success after config fix
   - GPU: `6`
   - accuracy `0.125`, format failure `0.250`
4. `qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_on`
   - status: success
   - GPU: `6`
   - accuracy `0.125`, format failure `0.125`
5. `qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_multigpu_smoke`
   - status: success
   - GPU: `6,7`
   - accuracy `0.500`, format failure `0.000`
6. `qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_strictfinal`
   - status: success
   - GPU: `6`
   - accuracy `0.000`, format failure `1.000`
7. `qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_off`
   - status: success
   - GPU: `6`
   - accuracy `0.375`, format failure `0.250`
8. `qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_minirun`
   - status: success
   - GPU: `6`
   - accuracy `0.40625`, format failure `0.000`
   - `num_items=32`
9. `qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off_minirun`
   - status: success
   - GPU: `6`
   - accuracy `0.125`, format failure `0.250`
   - `num_items=16`

## Analysis artifacts
- `results/analysis/latest_qwen3_runs.csv`
- `results/analysis/latest_qwen3_runs_canonical.csv`
- `results/analysis/direct_qwen3_pairs.csv`
- `results/analysis/direct_qwen3_pairs.json`
- `results/analysis/summary_overview.json`

## Current direct pairs
- GPQA canonical pair
  - off: accuracy `0.40625`, format failure `0.000`
  - on: accuracy `0.125`, format failure `0.875`
- GSM8K canonical pair
  - off: accuracy `0.375`, format failure `0.250`
  - on: accuracy `0.125`, format failure `0.125`

## Risks / blockers
- GPQA thinking-on remains dominated by formatting failure; prompt-only tightening did not fix it.
- GSM8K now has a direct off/on pair, but both runs are still small.
- AIME mini run confirms the benchmark path is stable enough to scale, but numeric ambiguity still persists.
- The generated sweep set exists, but a selective subset still needs to be launched to move from mini runs to broader coverage.

## Pending next priorities
1. Add parser-side fallback for Qwen3 thinking-on GPQA outputs
2. Launch first selective sweep subset from generated configs (`k in {0,2,4,8}`)
3. Expand GSM8K pair and AIME beyond current mini scale where useful
4. Validate one thinking-on config on `CUDA_VISIBLE_DEVICES=6,7`
