#!/usr/bin/env bash
set -euo pipefail
cd /data_x/aa007878/projects/crb
python - <<'PY'
import json
from pathlib import Path
for path in [
    Path('results_v2/manifests/status/workers.json'),
    Path('results_v2/manifests/status/queue_snapshot.json'),
    Path('results_v2/summary/bulk_coverage_summary.json'),
]:
    print(f'== {path} ==')
    if path.exists():
        print(path.read_text())
    else:
        print('(missing)')
PY
printf '\n== top active jobs ==\n'
python - <<'PY'
import csv
from pathlib import Path
path=Path('results_v2/manifests/status/job_status.csv')
if path.exists():
    rows=list(csv.DictReader(path.open()))
    active=[r for r in rows if r['status'] in {'queued','claimed','running','retry_wait'}]
    active=sorted(active, key=lambda r: (r['queue_name'], int(r['priority']), r['job_id']))
    for row in active[:20]:
        print(row['job_id'], row['queue_name'], row['status'], row['gpu_id'], row['retry_count'], row['failure_type'], row['config_path'])
else:
    print('(missing)')
PY
