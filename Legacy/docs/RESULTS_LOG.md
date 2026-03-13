# CRB Results Log

## 2026-03-10 / 2026-03-11 staged execution

### Stage 1–13 summary
- early smoke/mini runs established GPQA, GSM8K, and AIME execution paths
- preliminary aggregate tables were added under `results/analysis/`
- GPQA thinking-on rescue work identified `/no_think` + prefill as the usable full-scale path

## 2026-03-11 full-sample main-table core batch

### Stage 14: GPQA full-sample pair
- **thinking off**
  - config: `configs/generated/qwen3_main_table_full/qwen3_gpqa__thinking_off__main_table_full.yaml`
  - run: `run-20260311T095147Z-9780aeaf`
  - items: `448`
  - accuracy: `0.27232142857142855`
  - format failure: `0.008928571428571428`

- **thinking on (`/no_think` + prefill)**
  - config: `configs/generated/qwen3_main_table_full/qwen3_gpqa__thinking_on__main_table_full.yaml`
  - run: `run-20260311T095329Z-562ba8dc`
  - items: `448`
  - accuracy: `0.27232142857142855`
  - format failure: `0.026785714285714284`

### Stage 15: GSM8K full-sample pair
- **thinking off**
  - config: `configs/generated/qwen3_main_table_full/qwen3_gsm8k__thinking_off__main_table_full.yaml`
  - run: `run-20260311T115627Z-db8bf662`
  - items: `1319`
  - accuracy: `0.35178165276724793`
  - format failure: `0.18271417740712662`

- **thinking on**
  - config: `configs/generated/qwen3_main_table_full/qwen3_gsm8k__thinking_on__main_table_full.yaml`
  - run: `run-20260311T193631Z-270aebac`
  - items: `1319`
  - accuracy: `0.3889310083396513`
  - format failure: `0.1379833206974981`

### Stage 16: AIME full-sample pair
- **thinking off**
  - config: `configs/generated/qwen3_main_table_full/qwen3_aime__thinking_off__main_table_full.yaml`
  - run: `run-20260311T193920Z-b16718e7`
  - items: `30`
  - accuracy: `0.1`
  - format failure: `0.26666666666666666`

- **thinking on**
  - config: `configs/generated/qwen3_main_table_full/qwen3_aime__thinking_on__main_table_full.yaml`
  - run: `run-20260311T194547Z-1bb770a7`
  - items: `30`
  - accuracy: `0.03333333333333333`
  - format failure: `0.8333333333333334`

### Stage 17: refreshed aggregate artifacts
- Re-ran: `python scripts/aggregate_preliminary_results.py`
- Updated:
  - `results/analysis/latest_qwen3_runs.csv`
  - `results/analysis/latest_qwen3_runs_canonical.csv`
  - `results/analysis/direct_qwen3_pairs.csv`
  - `results/analysis/direct_qwen3_pairs.json`
  - `results/analysis/main_table_qwen3.csv`
  - `results/analysis/main_table_qwen3.json`
  - `results/analysis/summary_overview.json`

## 2026-03-12 follow-up execution

### Stage 18: MMLU full pair completion
- launched after the core batch
- **thinking off**
  - config: `configs/generated/qwen3_main_table_full/qwen3_mmlu__thinking_off__main_table_full.yaml`
  - GPU: `CUDA_VISIBLE_DEVICES=4`
  - run: `run-20260312T053743Z-b5f103ff`
  - items: `14042`
  - accuracy: `0.5883777239709443`
  - format failure: `0.0010682238997293833`
- **thinking on**
  - config: `configs/generated/qwen3_main_table_full/qwen3_mmlu__thinking_on__main_table_full.yaml`
  - GPU: `CUDA_VISIBLE_DEVICES=5,6`
  - run: `run-20260312T193756Z-f686300f`
  - items: `14042`
  - accuracy: `0.6664292835778379`
  - format failure: `0.021364477994587665`

## Current conclusion
- the CRB repository now has full-sample main-table rows for GPQA, GSM8K, AIME, and MMLU
- GSM8K and MMLU are the strongest current thinking-on wins
- GPQA thinking-on is rescued enough to be usable at full scale, but not better than thinking off
- AIME thinking-on remains unstable
