#!/usr/bin/env bash
set -euo pipefail

CONFIG_PATH="${1:?usage: $0 <config.yaml>}"
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-6}"
export HF_HOME="${HF_HOME:-/mnt/raid6/aa007878/.cache/huggingface}"
python -m crb.cli.run_eval --config "$CONFIG_PATH"
