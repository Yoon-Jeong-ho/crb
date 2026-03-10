#!/usr/bin/env bash
set -euo pipefail

export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-6,7}"
export HF_HOME="${HF_HOME:-/mnt/raid6/aa007878/.cache/huggingface}"
python -m crb.cli.run_batch "$@"
