#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo '== GPUs =='
nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu --format=csv,noheader

echo
echo '== Active run_eval =='
ps -eo pid,etimes,cmd | grep -E 'crb\.cli\.run_eval' | grep -v grep || true

echo
echo '== tmux sessions =='
tmux ls 2>/dev/null || true

echo
echo '== recent multimodel followup rows =='
python - <<'PY'
import csv
path='results/summary/scoreboard.csv'
rows=list(csv.DictReader(open(path)))
rows=[r for r in rows if r['history_mode']=='stored_history' and r['model_name'] in {
    'Qwen/Qwen2.5-1.5B-Instruct',
    'meta-llama/Llama-3.2-3B-Instruct',
    'mistralai/Mistral-7B-Instruct-v0.1',
}]
for row in rows[-20:]:
    print(row['run_id'], row['model_name'], row['dataset'], row['dummy_type'], row['k'], row['accuracy'], row['format_failure_rate'])
PY
