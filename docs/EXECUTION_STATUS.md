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
- [ ] Derived analysis artifacts have **not** been refreshed to match the latest scoreboard
- [ ] Two claim-relevant partial-only runs still need an explicit keep/complete vs archive decision

## Artifact snapshot

- `Legacy/results/summary/scoreboard.csv`
  - current rows: **573**
  - git state: modified locally; contains uncommitted appended result rows
- `analysis/tables/run_inventory.csv`
  - current rows: **308**
  - status: **stale relative to scoreboard**
- partial-only run directories: **2**
  1. `qwen3_1p7b_gsm8k_protocol_kfull_gsm8k_on_canonical_k4`
  2. `qwen3_1p7b_gsm8k_gsm8k_wrong_history_cross_domain_full_k8`

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

1. Refresh derived analysis from the current scoreboard
2. Classify current runs as main / secondary / parked
3. Decide whether the two stranded partial runs are keep-and-complete or archive
4. Only then decide the minimum next run set
