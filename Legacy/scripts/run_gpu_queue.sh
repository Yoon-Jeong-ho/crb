#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 [--gpus 4,5,6,7] [--poll-seconds 30] <config-or-dir>..." >&2
  exit 1
fi

GPU_LIST="4,5,6,7"
POLL_SECONDS=30
PYTHON_BIN="${PYTHON_BIN:-/data_x/aa007878/projects/crb/.conda/envs/crb/bin/python}"
export PYTHONNOUSERSITE="${PYTHONNOUSERSITE:-1}"
export HF_HOME="${HF_HOME:-/mnt/raid6/aa007878/.cache/huggingface}"

ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --gpus)
      GPU_LIST="${2:?missing value for --gpus}"
      shift 2
      ;;
    --poll-seconds)
      POLL_SECONDS="${2:?missing value for --poll-seconds}"
      shift 2
      ;;
    *)
      ARGS+=("$1")
      shift
      ;;
  esac
done

if [[ ${#ARGS[@]} -eq 0 ]]; then
  echo "run_gpu_queue.sh: no configs provided" >&2
  exit 1
fi

expand_configs() {
  local token
  for token in "$@"; do
    if [[ -d "$token" ]]; then
      find "$token" -maxdepth 1 -type f \( -name '*.yaml' -o -name '*.yml' \) | sort
    else
      printf '%s\n' "$token"
    fi
  done
}

pick_free_gpu() {
  local reserved_csv="${1:-}"
  "$PYTHON_BIN" - "$GPU_LIST" "$reserved_csv" <<'PY'
import subprocess
import sys

requested = [item.strip() for item in sys.argv[1].split(",") if item.strip()]
reserved = {item.strip() for item in sys.argv[2].split(",") if item.strip()}
gpu_rows = subprocess.check_output(
    ["nvidia-smi", "--query-gpu=index,uuid", "--format=csv,noheader,nounits"],
    text=True,
).splitlines()
uuid_by_index = {}
for row in gpu_rows:
    if not row.strip():
        continue
    index, uuid = [part.strip() for part in row.split(",", 1)]
    uuid_by_index[index] = uuid

busy = set()
proc = subprocess.run(
    ["nvidia-smi", "--query-compute-apps=gpu_uuid,pid", "--format=csv,noheader,nounits"],
    text=True,
    capture_output=True,
    check=False,
)
for row in proc.stdout.splitlines():
    if not row.strip():
        continue
    gpu_uuid, _pid = [part.strip() for part in row.split(",", 1)]
    for index, mapped_uuid in uuid_by_index.items():
        if mapped_uuid == gpu_uuid:
            busy.add(index)
            break

busy.update(reserved)

for gpu in requested:
    if gpu not in busy:
        print(gpu)
        raise SystemExit(0)

raise SystemExit(1)
PY
}

timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p logs/queue
queue_log="logs/queue/gpu_queue_${timestamp}.log"
touch "$queue_log"

declare -a CONFIGS=()
while IFS= read -r config_path; do
  [[ -n "$config_path" ]] || continue
  CONFIGS+=("$config_path")
done < <(expand_configs "${ARGS[@]}")

if [[ ${#CONFIGS[@]} -eq 0 ]]; then
  echo "run_gpu_queue.sh: no yaml configs resolved" >&2
  exit 1
fi

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] queue_start gpus=${GPU_LIST} configs=${#CONFIGS[@]} log=${queue_log}" | tee -a "$queue_log"

declare -A RESERVED_BY_PID=()
queue_failed=0

reserved_gpu_csv() {
  local values=()
  local pid
  for pid in "${!RESERVED_BY_PID[@]}"; do
    values+=("${RESERVED_BY_PID[$pid]}")
  done
  IFS=,
  echo "${values[*]}"
}

launch_config() {
  local gpu="$1"
  local config_path="$2"
  local config_base
  config_base="$(basename "${config_path%.*}")"
  local run_log="logs/queue/${timestamp}__gpu${gpu}__${config_base}.log"
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] launch gpu=${gpu} config=${config_path} run_log=${run_log}" | tee -a "$queue_log"
  (
    export CUDA_VISIBLE_DEVICES="$gpu"
    bash scripts/run_single_gpu.sh "$config_path"
  ) >"$run_log" 2>&1 &
  RESERVED_BY_PID[$!]="$gpu"
}

reap_finished_children() {
  local pid
  for pid in "${!RESERVED_BY_PID[@]}"; do
    if ! kill -0 "$pid" 2>/dev/null; then
      if ! wait "$pid"; then
        queue_failed=1
      fi
      echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] release gpu=${RESERVED_BY_PID[$pid]} pid=${pid}" | tee -a "$queue_log"
      unset 'RESERVED_BY_PID[$pid]'
    fi
  done
}

for config_path in "${CONFIGS[@]}"; do
  while true; do
    reap_finished_children
    if free_gpu="$(pick_free_gpu "$(reserved_gpu_csv)" 2>/dev/null)"; then
      launch_config "$free_gpu" "$config_path"
      break
    fi
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] wait_no_free_gpu config=${config_path} poll=${POLL_SECONDS}s" | tee -a "$queue_log"
    sleep "$POLL_SECONDS"
  done
done

while [[ ${#RESERVED_BY_PID[@]} -gt 0 ]]; do
  reap_finished_children
  if [[ ${#RESERVED_BY_PID[@]} -gt 0 ]]; then
    sleep 2
  fi
done

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] queue_done failed=${queue_failed}" | tee -a "$queue_log"
exit "$queue_failed"
