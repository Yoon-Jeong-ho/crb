#!/usr/bin/env bash
set -euo pipefail
GPU_SET="$1"
CFG_PATH="$2"
LOG_PATH="$3"
cd /data_x/aa007878/projects/crb
while true; do
  busy=0
  IFS=',' read -ra ids <<< "$GPU_SET"
  for id in "${ids[@]}"; do
    used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits -i "$id" | tr -d ' ')
    if [ "${used}" -gt 200 ]; then
      busy=1
      break
    fi
  done
  if [ "$busy" -eq 0 ]; then
    break
  fi
  echo "[wait] $(date -u +%FT%TZ) waiting for gpus=${GPU_SET} cfg=${CFG_PATH}" | tee -a "$LOG_PATH"
  sleep 30
done
echo "[queue] $(date -u +%FT%TZ) start gpus=${GPU_SET} cfg=${CFG_PATH}" | tee -a "$LOG_PATH"
env -u LD_LIBRARY_PATH CUDA_VISIBLE_DEVICES="$GPU_SET" PYTHONNOUSERSITE=1 \
  /data_x/aa007878/projects/crb/.conda/envs/crb/bin/python -m crb_v2.cli --config "$CFG_PATH" \
  2>&1 | tee -a "$LOG_PATH"
echo "[queue] $(date -u +%FT%TZ) finish gpus=${GPU_SET} cfg=${CFG_PATH}" | tee -a "$LOG_PATH"
