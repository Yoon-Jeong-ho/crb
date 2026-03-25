#!/usr/bin/env bash
set -euo pipefail
cd /data_x/aa007878/projects/crb
PYTHONNOUSERSITE=1 /data_x/aa007878/projects/crb/.conda/envs/crb/bin/python tools/crb_v2_prepare_wave.py
