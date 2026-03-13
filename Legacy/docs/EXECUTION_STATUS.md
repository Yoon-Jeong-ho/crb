# CRB Execution Status

_Last updated: 2026-03-12_

## Current environment
- Project root: `/data_x/aa007878/projects/crb`
- Execution env: `/data_x/aa007878/projects/crb/.conda/envs/crb`
- Python: `3.10.19`
- torch: `2.9.0+cu128`
- transformers: `4.57.6`
- vllm: `0.11.2`
- datasets: `2.21.0`
- Branch: `main`

## GPU policy / current usage
- Current operator-allowed GPUs: `4,5,6`
- Main-table core full batch on GPUs `5,6` is complete.
- MMLU full pair was launched after the core batch:
  - thinking off: `CUDA_VISIBLE_DEVICES=4`
  - thinking on: `CUDA_VISIBLE_DEVICES=5,6`

## Main-table core batch status

### Completed full-sample rows
1. **GPQA / Qwen3 thinking off**
   - run: `run-20260311T095147Z-9780aeaf`
   - items: `448`
   - accuracy `0.27232142857142855`
   - format failure `0.008928571428571428`

2. **GPQA / Qwen3 thinking on (`/no_think` + prefill)**
   - run: `run-20260311T095329Z-562ba8dc`
   - items: `448`
   - accuracy `0.27232142857142855`
   - format failure `0.026785714285714284`

3. **GSM8K / Qwen3 thinking off**
   - run: `run-20260311T115627Z-db8bf662`
   - items: `1319`
   - accuracy `0.35178165276724793`
   - format failure `0.18271417740712662`

4. **GSM8K / Qwen3 thinking on**
   - run: `run-20260311T193631Z-270aebac`
   - items: `1319`
   - accuracy `0.3889310083396513`
   - format failure `0.1379833206974981`

5. **AIME / Qwen3 thinking off**
   - run: `run-20260311T193920Z-b16718e7`
   - items: `30`
   - accuracy `0.1`
   - format failure `0.26666666666666666`

6. **AIME / Qwen3 thinking on**
   - run: `run-20260311T194547Z-1bb770a7`
   - items: `30`
   - accuracy `0.03333333333333333`
   - format failure `0.8333333333333334`

### MMLU state
- smoke validation completed:
  - off: `run-20260311T094321Z-b9d8f324`
  - on: `run-20260311T094535Z-26b1aa1b`
- full pair completed:
  - off: `run-20260312T053743Z-b5f103ff`
  - on: `run-20260312T193756Z-f686300f`
  - items: `14042 / 14042`
  - off accuracy `0.5883777239709443`, format failure `0.0010682238997293833`
  - on accuracy `0.6664292835778379`, format failure `0.021364477994587665`

## Analysis artifacts
- `results/analysis/latest_qwen3_runs.csv`
- `results/analysis/latest_qwen3_runs_canonical.csv`
- `results/analysis/direct_qwen3_pairs.csv`
- `results/analysis/direct_qwen3_pairs.json`
- `results/analysis/main_table_qwen3.csv`
- `results/analysis/main_table_qwen3.json`
- `results/analysis/summary_overview.json`

## Current full-sample direct pairs
- **GPQA / multi_turn / oracle_history / same_domain / k=2**
  - off: accuracy `0.2723`, format failure `0.0089`
  - on: accuracy `0.2723`, format failure `0.0268`

- **GSM8K / single_turn_flattened / self_history / cross_domain / k=2**
  - off: accuracy `0.3518`, format failure `0.1827`
  - on: accuracy `0.3889`, format failure `0.1380`

- **AIME / multi_turn / oracle_history / same_domain / k=2**
  - off: accuracy `0.1000`, format failure `0.2667`
  - on: accuracy `0.0333`, format failure `0.8333`


- **MMLU / multi_turn / oracle_history / same_domain / k=2**
  - off: accuracy `0.5884`, format failure `0.0011`
  - on: accuracy `0.6664`, format failure `0.0214`

## Current interpretation
- GPQA thinking-on no longer collapses the way the early smoke runs did, but it still does **not** outperform thinking-off.
- GSM8K is the strongest current case for a beneficial thinking-on effect in the main-table setting.
- AIME thinking-on is currently not a viable main-table path.
- The core paper-table rows are now full-sample for **GPQA/GSM8K/AIME/MMLU**.
- MMLU full-sample results materially strengthen the current main table because they add a large-breadth anchor benchmark.

## Pending next priorities
1. Add per-dataset error breakdowns on top of the finished four-benchmark main table.
2. Launch the first selective `k={0,2,4,8}` subset on the strongest current lanes.
3. Decide whether AIME thinking-on should stay in the headline table or move to a failure-case appendix.
4. Sync root-level docs with the new four-benchmark full-sample state.
