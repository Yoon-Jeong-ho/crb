#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "== tmux sessions =="
tmux ls 2>/dev/null | grep 'crb-singleturn-chain' || true

echo
echo "== queue processes =="
ps -ef | grep -E 'run_qwen3_single_turn_full_chain|run_gpu_queue|single_turn_pool|stored_(correct|incorrect)_same_k2_smoke' | grep -v grep || true

echo
echo "== gpu compute apps =="
nvidia-smi --query-compute-apps=gpu_uuid,pid,process_name,used_gpu_memory --format=csv,noheader || true

echo
echo "== latest chain log =="
latest_log="$(ls -1t logs/queue/gpu_queue_*.log 2>/dev/null | head -n 1 || true)"
if [[ -n "$latest_log" ]]; then
  echo "$latest_log"
  tail -n 25 "$latest_log"
else
  echo "no queue log"
fi

echo
echo "== latest pool summaries =="
python - <<'PY'
from pathlib import Path
import json
root = Path("results/pools/single_turn/qwen3_1p7b")
for summary in sorted(root.glob("**/summary.json")):
    data = json.loads(summary.read_text())
    print(summary)
    print({k: data.get(k) for k in ["run_id", "dataset_name", "split", "thinking_mode", "total_items", "format_valid_items", "correct_items", "incorrect_items"]})
PY
