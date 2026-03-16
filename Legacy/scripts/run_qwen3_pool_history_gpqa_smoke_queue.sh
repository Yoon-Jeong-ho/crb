#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

CORRECT_POOL="results/pools/single_turn/qwen3_1p7b/thinking_off/gpqa/train/correct.jsonl"
INCORRECT_POOL="results/pools/single_turn/qwen3_1p7b/thinking_off/gpqa/train/incorrect.jsonl"

bash scripts/run_when_files_exist.sh \
  --poll-seconds "${POLL_SECONDS:-60}" \
  "$CORRECT_POOL" \
  "$INCORRECT_POOL" \
  -- \
  bash scripts/run_gpu_queue.sh \
    --gpus "${GPU_LIST:-4,5,6,7}" \
    --poll-seconds "${GPU_POLL_SECONDS:-30}" \
    configs/pool_history/qwen3_1p7b_gpqa_multiturn_stored_correct_same_k2_smoke.yaml \
    configs/pool_history/qwen3_1p7b_gpqa_multiturn_stored_incorrect_same_k2_smoke.yaml
