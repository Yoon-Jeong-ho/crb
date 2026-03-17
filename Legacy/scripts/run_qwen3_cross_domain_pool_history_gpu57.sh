#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

PYTHON_BIN="${PYTHON_BIN:-/data_x/aa007878/projects/crb/.conda/envs/crb/bin/python}"
$PYTHON_BIN -m crb.cli.materialize_sweep --spec configs/sweeps/qwen3_cross_domain_pool_history.yaml >/dev/null

bash scripts/run_gpu_queue.sh \
  --gpus "${GPU_LIST:-5,7}" \
  --poll-seconds "${POLL_SECONDS:-30}" \
  configs/generated/qwen3_cross_domain_pool_history
