#!/usr/bin/env bash
set -euo pipefail

bash scripts/materialize_qwen3_core_sweep.sh
bash scripts/run_batch.sh configs/generated/qwen3_core_paper
