#!/usr/bin/env bash
set -euo pipefail

# Main-table batch focuses on the currently paper-core benchmark rows:
# GPQA, GSM8K, and AIME.
# A full MMLU all-sample on/off pair is prepared separately but is not part of
# this core batch because it is materially longer on the currently available GPUs.

bash scripts/materialize_qwen3_main_table_full.sh
bash scripts/run_batch.sh \
  configs/generated/qwen3_main_table_full/qwen3_gpqa__thinking_off__main_table_full.yaml \
  configs/generated/qwen3_main_table_full/qwen3_gpqa__thinking_on__main_table_full.yaml \
  configs/generated/qwen3_main_table_full/qwen3_gsm8k__thinking_off__main_table_full.yaml \
  configs/generated/qwen3_main_table_full/qwen3_gsm8k__thinking_on__main_table_full.yaml \
  configs/generated/qwen3_main_table_full/qwen3_aime__thinking_off__main_table_full.yaml \
  configs/generated/qwen3_main_table_full/qwen3_aime__thinking_on__main_table_full.yaml
