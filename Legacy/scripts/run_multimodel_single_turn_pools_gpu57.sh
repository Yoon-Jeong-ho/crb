#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

PYTHON_BIN="${PYTHON_BIN:-/data_x/aa007878/projects/crb/.conda/envs/crb/bin/python}"
$PYTHON_BIN scripts/materialize_multimodel_pool_workflows.py >/dev/null

bash scripts/run_gpu_queue.sh \
  --gpus "${GPU_LIST:-5,7}" \
  --poll-seconds "${POLL_SECONDS:-30}" \
  configs/generated/multimodel_single_turn_pools/qwen25_1p5b \
  configs/generated/multimodel_single_turn_pools/llama32_3b \
  configs/generated/multimodel_single_turn_pools/mistral7b
