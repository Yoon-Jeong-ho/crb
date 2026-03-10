#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-/data_x/aa007878/projects/crb/.conda/envs/crb/bin/python}"
export PYTHONNOUSERSITE="${PYTHONNOUSERSITE:-1}"

$PYTHON_BIN -m crb.cli.materialize_sweep --spec configs/sweeps/qwen3_core_paper.yaml
