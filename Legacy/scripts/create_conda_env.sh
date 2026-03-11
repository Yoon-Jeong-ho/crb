#!/usr/bin/env bash
set -euo pipefail

ENV_PREFIX="/data_x/aa007878/projects/crb/.conda/envs/crb"
export PYTHONNOUSERSITE="${PYTHONNOUSERSITE:-1}"

if [[ ! -x "$ENV_PREFIX/bin/python" ]]; then
  CONDA_NO_PLUGINS=true conda create -y -p "$ENV_PREFIX" python=3.10 pip
fi

"$ENV_PREFIX/bin/pip" install -r requirements.txt
"$ENV_PREFIX/bin/pip" install -e .

echo "Environment ready: $ENV_PREFIX"
