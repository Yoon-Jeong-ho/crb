#!/usr/bin/env bash
set -uo pipefail
GPU_SET="$1"
QUEUE_FILE="$2"
LOG_PATH="$3"
cd /data_x/aa007878/projects/crb
while IFS= read -r cfg; do
  [ -z "$cfg" ] && continue
  echo "[queue] $(date -u +%FT%TZ) start gpus=${GPU_SET} cfg=${cfg}" | tee -a "$LOG_PATH"
  set +e
  env -u LD_LIBRARY_PATH CUDA_VISIBLE_DEVICES="$GPU_SET" PYTHONNOUSERSITE=1 \
    /data_x/aa007878/projects/crb/.conda/envs/crb/bin/python -m crb_v2.cli --config "$cfg" \
    2>&1 | tee -a "$LOG_PATH"
  exit_code=${PIPESTATUS[0]}
  set -e
  echo "[queue] $(date -u +%FT%TZ) finish gpus=${GPU_SET} cfg=${cfg} exit=${exit_code}" | tee -a "$LOG_PATH"
  sleep 10
done < "$QUEUE_FILE"
