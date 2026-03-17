#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

run_lane() {
  local gpu="$1"
  shift
  local cfg
  local timestamp
  timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
  mkdir -p logs/queue
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

gpu5_cfgs=(
  "configs/pool_history/qwen3_1p7b_gpqa_multiturn_stored_correct_same_k2_thinking_on_nothink_prefill.yaml"
  "configs/pool_history/qwen3_1p7b_gpqa_multiturn_stored_correct_same_k4_thinking_on_nothink_prefill.yaml"
  "configs/pool_history/qwen3_1p7b_gpqa_multiturn_stored_correct_same_k8_thinking_on_nothink_prefill.yaml"
  "configs/pool_history/qwen3_1p7b_gpqa_multiturn_stored_correct_same_k16_thinking_on_nothink_prefill.yaml"
)

gpu7_cfgs=(
  "configs/pool_history/qwen3_1p7b_gpqa_multiturn_stored_incorrect_same_k2_thinking_on_nothink_prefill.yaml"
  "configs/pool_history/qwen3_1p7b_gpqa_multiturn_stored_incorrect_same_k4_thinking_on_nothink_prefill.yaml"
  "configs/pool_history/qwen3_1p7b_gpqa_multiturn_stored_incorrect_same_k8_thinking_on_nothink_prefill.yaml"
  "configs/pool_history/qwen3_1p7b_gpqa_multiturn_stored_incorrect_same_k16_thinking_on_nothink_prefill.yaml"
)

run_lane 5 "${gpu5_cfgs[@]}" &
pid5=$!
run_lane 7 "${gpu7_cfgs[@]}" &
pid7=$!

wait "$pid5"
wait "$pid7"
