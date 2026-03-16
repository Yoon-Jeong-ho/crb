#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

bash scripts/run_gpu_queue.sh \
  --gpus "${GPU_LIST:-4,5,6,7}" \
  --poll-seconds "${POLL_SECONDS:-30}" \
  configs/single_turn_pool/qwen3_1p7b_gpqa_single_turn_pool_thinking_on_nothink_prefill.yaml \
  configs/single_turn_pool/qwen3_1p7b_gsm8k_single_turn_pool_thinking_on.yaml \
  configs/single_turn_pool/qwen3_1p7b_mmlu_single_turn_pool_thinking_on.yaml \
  configs/single_turn_pool/qwen3_1p7b_aime_single_turn_pool_thinking_on.yaml
