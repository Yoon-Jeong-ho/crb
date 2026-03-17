#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

export PYTHONNOUSERSITE="${PYTHONNOUSERSITE:-1}"
export HF_HOME="${HF_HOME:-/mnt/raid6/aa007878/.cache/huggingface}"
PYTHON_BIN="${PYTHON_BIN:-/data_x/aa007878/projects/crb/.conda/envs/crb/bin/python}"

launch_bg() {
  local gpu="$1"
  local config="$2"
  local run_log="$3"
  (
    export CUDA_VISIBLE_DEVICES="$gpu"
    bash scripts/run_single_gpu.sh "$config"
  ) >"$run_log" 2>&1 &
  echo $!
}

mkdir -p logs/queue
timestamp="$(date -u +%Y%m%dT%H%M%SZ)"

gpu5_cfgs=(
  "configs/pool_history/qwen3_1p7b_gpqa_multiturn_stored_correct_same_k2.yaml"
  "configs/pool_history/qwen3_1p7b_gpqa_multiturn_stored_correct_same_k4.yaml"
  "configs/pool_history/qwen3_1p7b_gpqa_multiturn_stored_correct_same_k8.yaml"
  "configs/pool_history/qwen3_1p7b_gpqa_multiturn_stored_correct_same_k16.yaml"
)

gpu7_cfgs=(
  "configs/pool_history/qwen3_1p7b_gpqa_multiturn_stored_incorrect_same_k2.yaml"
  "configs/pool_history/qwen3_1p7b_gpqa_multiturn_stored_incorrect_same_k4.yaml"
  "configs/pool_history/qwen3_1p7b_gpqa_multiturn_stored_incorrect_same_k8.yaml"
  "configs/pool_history/qwen3_1p7b_gpqa_multiturn_stored_incorrect_same_k16.yaml"
)

run_lane() {
  local gpu="$1"
  shift
  local cfg
  for cfg in "$@"; do
    local base
    base="$(basename "${cfg%.*}")"
    local log_path="logs/queue/${timestamp}__gpu${gpu}__${base}.log"
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] launch gpu=${gpu} config=${cfg} log=${log_path}"
    export CUDA_VISIBLE_DEVICES="$gpu"
    bash scripts/run_single_gpu.sh "$cfg" >"$log_path" 2>&1
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] complete gpu=${gpu} config=${cfg}"
  done
}

run_lane 5 "${gpu5_cfgs[@]}" &
pid5=$!
run_lane 7 "${gpu7_cfgs[@]}" &
pid7=$!

wait "$pid5"
wait "$pid7"
