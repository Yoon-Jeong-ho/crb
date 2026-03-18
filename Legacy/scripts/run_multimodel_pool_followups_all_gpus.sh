#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

PYTHON_BIN="${PYTHON_BIN:-/data_x/aa007878/projects/crb/.conda/envs/crb/bin/python}"
GPU_LIST="${GPU_LIST:-0,1,2,3,4,5,6,7}"
POLL_SECONDS="${POLL_SECONDS:-30}"
MODELS=("${@}")
if [[ ${#MODELS[@]} -eq 0 ]]; then
  MODELS=(qwen25_1p5b llama32_3b mistral7b)
fi

$PYTHON_BIN scripts/materialize_multimodel_pool_workflows.py >/dev/null

ARGS=()
for model in "${MODELS[@]}"; do
  ARGS+=("configs/generated/multimodel_pool_followups/${model}")
done

bash scripts/run_gpu_queue.sh \
  --gpus "$GPU_LIST" \
  --poll-seconds "$POLL_SECONDS" \
  "${ARGS[@]}"
