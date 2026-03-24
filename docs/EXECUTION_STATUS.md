# EXECUTION STATUS

- Date: 2026-03-20
- Status: **claim-first freeze**
- Active rule: **do not widen experiment scope until docs, derived analysis, and partial-run decisions are synchronized**

## Current state

- [x] `Legacy/` remains the only authoritative runnable CRB tree
- [x] The canonical headline baseline is now fixed as:
  - `single_turn`, `k=0`, no dummy history
- [x] `stored_history` is now explicitly interpreted as:
  - **external contaminated-history robustness**
  - not a hidden rename of `self_history`
- [x] Multimodel baseline + `stored_history` follow-up runs now exist on disk
- [x] Qwen3 full-sample baseline rows exist for `gpqa`, `gsm8k`, `aime`, and `mmlu`
- [x] Qwen3 full-sample follow-up slices exist for several main protocol conditions
- [x] Derived analysis artifacts have been refreshed to match the latest scoreboard
- [x] The two claim-relevant appendix reruns are now complete

## Artifact snapshot

- `Legacy/results/summary/scoreboard.csv`
  - current rows: **576**
  - git state: modified locally; contains uncommitted appended result rows
- `analysis/tables/run_inventory.csv`
  - current rows: **576**
  - status: refreshed after appendix closure
- appendix closure rows now exist:
  1. `run-20260323T143713Z-85b1af5d` — `self_history / k=4`
  2. `run-20260323T120127Z-b3c43227` — `wrong_history / k=8`
  3. `run-20260324T044142Z-1e65b909` — `self_history / k=8` (optional appendix extension)

## Strongest currently usable evidence classes

1. **Canonical single-turn baselines**
   - `qwen3` off/on across `gpqa`, `gsm8k`, `aime`, `mmlu`
   - `qwen25`, `llama32_3b`, `mistral7b` off across the same set
2. **Qwen3 full-sample provenance slices**
   - `gpqa`: oracle / wrong / stored
   - `gsm8k`: flattened self / wrong, plus stored off-lane
   - `mmlu`: oracle
3. **Multimodel stored-history slices**
   - baseline + `stored_history` across `gpqa`, `gsm8k`, `aime`, `mmlu`

## What is no longer the main blocker

The repo is no longer blocked mainly by:

- “can the pipeline run?”
- “can Qwen3 produce a final answer at all?”

The main blocker is now:

**whether the existing artifact set has been classified and summarized correctly under the frozen CRB claim.**

## Immediate next actions

1. Main/supporting figure work can now proceed from the refreshed analysis outputs
2. Appendix figure work can now also proceed from the refreshed analysis outputs
3. No appendix rerun gap remains; next work is drafting/packaging rather than more runs
