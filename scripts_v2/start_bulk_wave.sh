#!/usr/bin/env bash
set -euo pipefail
cd /data_x/aa007878/projects/crb
if pgrep -af 'tools/crb_v2_bulk_supervisor.py worker' >/dev/null; then
  echo 'bulk workers already running; refusing duplicate launch' >&2
  pgrep -af 'tools/crb_v2_bulk_supervisor.py worker' >&2 || true
  exit 1
fi
PYTHONNOUSERSITE=1 /data_x/aa007878/projects/crb/.conda/envs/crb/bin/python tools/crb_v2_bulk_supervisor.py start
