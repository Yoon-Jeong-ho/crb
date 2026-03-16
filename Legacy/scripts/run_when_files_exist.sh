#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "usage: $0 [--poll-seconds 30] <file> <file> -- <command...>" >&2
  exit 1
fi

POLL_SECONDS=30
REQUIRED=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --poll-seconds)
      POLL_SECONDS="${2:?missing value for --poll-seconds}"
      shift 2
      ;;
    --)
      shift
      break
      ;;
    *)
      REQUIRED+=("$1")
      shift
      ;;
  esac
done

if [[ ${#REQUIRED[@]} -eq 0 || $# -eq 0 ]]; then
  echo "run_when_files_exist.sh: missing required files or command" >&2
  exit 1
fi

while true; do
  missing=0
  for path in "${REQUIRED[@]}"; do
    if [[ ! -f "$path" ]]; then
      missing=1
      break
    fi
  done
  if [[ "$missing" -eq 0 ]]; then
    break
  fi
  printf '[%s] waiting for pool files: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "${REQUIRED[*]}"
  sleep "$POLL_SECONDS"
done

exec "$@"
