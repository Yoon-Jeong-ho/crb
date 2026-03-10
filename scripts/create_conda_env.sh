#!/usr/bin/env bash
set -euo pipefail

CONDA_NO_PLUGINS=true conda env create -f environment.yml || \
CONDA_NO_PLUGINS=true conda env update -f environment.yml --prune

echo "Activate with: conda activate crb"
echo "Then install editable package: pip install -e ."
