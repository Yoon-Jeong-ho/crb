# RESULT

- Date: 2026-03-24
- Shareable snapshot rows: 120
- Scoreboard rows captured in this snapshot: 581

## Figure readiness

- Main: YES
- Supporting: YES
- Appendix: YES

## Key analysis so far

### Main: multimodel / stored_history / external contamination

- `llama` average Δ vs single-turn k=0: `-0.0197` (min `-0.0599`, max `0.0558`)
- `mistral` average Δ vs single-turn k=0: `0.1269` (min `0.0000`, max `0.2846`)
- `qwen25` average Δ vs single-turn k=0: `-0.0652` (min `-0.4352`, max `0.1168`)

Interpretation:
- model family reacts differently to externally injected stored-history contamination
- qwen25 is net negative, llama is mildly negative, and mistral is net positive in the current completed main slice

### Supporting: Qwen3 / GPQA / provenance

- strongest positive supporting row so far: `stored_incorrect / k=4` with accuracy `0.29464285714285715` and Δ `0.06919642857142858`
- same-domain provenance conditions are not uniformly harmful; several are above the single-turn baseline

### Appendix: Qwen3 / GSM8K / self-vs-wrong

- `self / k=0` → accuracy `0.6353297952994693`, Δ `-0.04473085670962851`, format-failure `0.0576194086429113`
- `self / k=2` → accuracy `0.3889310083396513`, Δ `-0.29112964366944655`, format-failure `0.1379833206974981`
- `self / k=4` → accuracy `0.3639120545868082`, Δ `-0.3161485974222896`, format-failure `0.07733131159969674`
- `wrong / k=2` → accuracy `0.3813495072024261`, Δ `-0.2987111448066717`, format-failure `0.1106899166034875`
- `wrong / k=4` → accuracy `0.36770280515542075`, Δ `-0.31235784685367707`, format-failure `0.04169825625473844`
- `wrong / k=8` → accuracy `0.33965125094768767`, Δ `-0.34040940106141016`, format-failure `0.02577710386656558`
- `self / k=8` → accuracy `0.310841546626232`, Δ `-0.36921910538286584`, format-failure `0.04169825625473844`

- worst appendix row is `self / k=8` with Δ `-0.36921910538286584`
- this appendix slice most directly shows that accumulated conversation history can sharply reduce final-turn target accuracy

## Newly completed broad backfill runs (shareable)

- `run-20260324T050441Z-a02c523e` — `llama / aime / single_turn / k=0` accuracy `0.06666666666666667`, format-failure `0.3333333333333333`
- `run-20260324T051159Z-3a804857` — `mistral / aime / single_turn / k=0` accuracy `0.0`, format-failure `0.8`
- `run-20260324T051316Z-a0f54d2b` — `llama / gpqa / single_turn / k=0` accuracy `0.23660714285714285`, format-failure `0.12053571428571429`
- `run-20260324T051809Z-47f05ae6` — `mistral / gpqa / single_turn / k=0` accuracy `0.11830357142857142`, format-failure `0.640625`
- `run-20260324T051905Z-681c31be` — `qwen25 / aime / single_turn / k=0` accuracy `0.0`, format-failure `0.23333333333333334`

## Active queue snapshot

- GPU 2: queue finished for the current AIME lane set
- GPU 5: GPQA baseline queue still active
- GPU 6: GSM8K baseline queue still active
- GPU 7: MMLU baseline queue still active

## Shareable files

- `RESULT.md`
- `result_snapshot.csv`
- `analysis/tables/main_multimodel_external_contamination.csv`
- `analysis/tables/supporting_qwen3_gpqa_provenance.csv`
- `analysis/tables/appendix_qwen3_gsm8k_self_vs_wrong.csv`
- `analysis/tables/run_inventory.csv`
- `docs/ANALYSIS.md`
