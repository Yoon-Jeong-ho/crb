#!/usr/bin/env bash
set -euo pipefail
cd /data_x/aa007878/projects/crb
LOG_PATH="logs/crb_v2_gpu2_pilot_$(date -u +%Y%m%dT%H%M%SZ).log"
echo "[pilot] $(date -u +%FT%TZ) starting GPU2 pilot" | tee -a "$LOG_PATH"
env -u LD_LIBRARY_PATH CUDA_VISIBLE_DEVICES=2 PYTHONNOUSERSITE=1 \
  /data_x/aa007878/projects/crb/.conda/envs/crb/bin/python \
  -m crb_v2.cli --config configs_v2/pilot/two_models_two_benchmarks.yaml \
  2>&1 | tee -a "$LOG_PATH"
echo "[pilot] $(date -u +%FT%TZ) finished GPU2 pilot" | tee -a "$LOG_PATH"
