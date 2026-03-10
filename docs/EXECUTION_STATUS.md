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
  - `6709d70` run qwen3 gpqa and aime smoke validations
  - `e6db683` add gpqa aime and qwen3 thinking sweep support
  - `5a986c3` validate local conda env and gpu-backed vllm runs

## GPU availability
- Policy GPUs: `6,7` only
- Check command:
  - `nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader`
- Most recent snapshot during this cycle:
  - GPU 6: `4 MiB / 49140 MiB`, util `0%`
  - GPU 7: `4 MiB / 49140 MiB`, util `0%`
- Decision:
  - smoke and follow-up runs were safe on GPU 6
  - one dedicated multi-GPU smoke run was also completed on GPUs 6 and 7

## Ready configs
- `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off.yaml`
- `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on.yaml`
- `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_strictfinal.yaml`
- `configs/qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_off.yaml`
- `configs/qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_on.yaml`
- `configs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off.yaml`
- `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_multigpu_smoke.yaml`

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

## Additional completed workflow steps
- scoreboard migration to include `model_family` and `thinking_mode`
- Qwen3 / GPQA / AIME result JSON validation
- paper sweep materialization executed successfully
  - generated configs: `256`
  - location: `configs/generated/qwen3_core_paper/`
- pytest re-run after test isolation fix
  - result: `8 passed`

## Risks / blockers
- Qwen3 thinking-on is not simply “harder”; on GPQA it is currently primarily a **formatting failure mode**.
- A stricter final-answer prompt did **not** rescue GPQA thinking-on; it made parse behavior worse in the smoke run.
- GSM8K thinking-on is much more parser-stable than GPQA thinking-on, suggesting the failure is not a universal parser bug.
- AIME numeric parsing works, but ambiguous numeric generations still occur.
- Current evidence remains smoke-scale (`num_samples=8`, multigpu smoke `num_samples=2`).

## Pending runs / next priorities
1. GPQA thinking-off and AIME mini runs with larger `num_samples`
2. Qwen3 thinking-off vs thinking-on on GSM8K side-by-side for cleaner comparison
3. AIME prompt or parser refinement for ambiguous numeric outputs
4. Materialized sweep subset launch for `k in {0,2,4,8}`
5. Multi-GPU validation for one thinking-on config
