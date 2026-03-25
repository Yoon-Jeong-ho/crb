#!/usr/bin/env bash
set -euo pipefail
MODE="${1:-smoke}"
ROOT="/data_x/aa007878/projects/crb"
PYTHON="${ROOT}/.conda/envs/crb/bin/python"
QUEUE_RUNNER="${ROOT}/scripts_v2/queues/run_config_queue.sh"
WAIT_RUNNER="${ROOT}/scripts_v2/queues/run_when_gpus_free.sh"
cd "$ROOT"

mkdir -p logs/crb_v2/gpu4 logs/crb_v2/gpu5 logs/crb_v2/gpu6 logs/crb_v2/gpu7
"${ROOT}/scripts_v2/refresh_v2_inventory.sh" >/dev/null

case "$MODE" in
  smoke)
    TS=$(date -u +%Y%m%dT%H%M%SZ)
    GPU4_CFG=$(sed -n '1p' results_v2/manifests/queues/gpu4_smoke.txt)
    GPU5_CFG=$(sed -n '1p' results_v2/manifests/queues/gpu5_smoke.txt)
    [ -n "$GPU4_CFG" ] || { echo "gpu4 smoke queue is empty"; exit 1; }
    [ -n "$GPU5_CFG" ] || { echo "gpu5 smoke queue is empty"; exit 1; }
    nohup bash "$WAIT_RUNNER" 4 "$GPU4_CFG" "logs/crb_v2/gpu4/smoke_${TS}.log" >/dev/null 2>&1 &
    PID4=$!
    sleep 10
    nohup bash "$WAIT_RUNNER" 5 "$GPU5_CFG" "logs/crb_v2/gpu5/smoke_${TS}.log" >/dev/null 2>&1 &
    PID5=$!
    echo "mode=smoke gpu4_pid=$PID4 gpu5_pid=$PID5"
    echo "gpu4_log=logs/crb_v2/gpu4/smoke_${TS}.log"
    echo "gpu5_log=logs/crb_v2/gpu5/smoke_${TS}.log"
    ;;
  bulk)
    TS=$(date -u +%Y%m%dT%H%M%SZ)
    nohup bash "$QUEUE_RUNNER" 6 results_v2/manifests/queues/gpu6_bulk.txt "logs/crb_v2/gpu6/bulk_${TS}.log" >/dev/null 2>&1 &
    PID6=$!
    sleep 10
    nohup bash "$QUEUE_RUNNER" 7 results_v2/manifests/queues/gpu7_bulk.txt "logs/crb_v2/gpu7/bulk_${TS}.log" >/dev/null 2>&1 &
    PID7=$!
    echo "mode=bulk gpu6_pid=$PID6 gpu7_pid=$PID7"
    echo "gpu6_log=logs/crb_v2/gpu6/bulk_${TS}.log"
    echo "gpu7_log=logs/crb_v2/gpu7/bulk_${TS}.log"
    echo "retry_queue=results_v2/manifests/queues/retry_queue.txt"
    ;;
  *)
    echo "usage: $0 [smoke|bulk]" >&2
    exit 1
    ;;
esac
