# LEGACY NOTES

- Date: 2026-03-11

## Stable facts

- `Legacy/` still contains the only runnable CRB code/config/test tree.
- Earlier same-day GPQA thinking-off smoke reruns on GPU4 are already preserved as baseline evidence.
- The current stable pushed doc checkpoint is `28e4058` + `02fa431`.
- The GPU567 continuation branch now also has one fresh parserfix smoke result: `run-20260311T060823Z-1947f5cf` on GPU 5.

## Current continuation-specific rule

- For `crb-gpu567-continuation-gpus-5`, **fresh work uses GPUs `5,6,7` only**.
- Therefore GPU4 evidence remains historical reference, not the launch target for new continuation jobs.

## Active local WIP to watch

- parserfix worktree currently touches:
  - `Legacy/src/crb/evaluation/parsers.py`
  - `Legacy/tests/test_parsers.py`
  - `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix.yaml`
- Current status: verified once on GPU5, but still only `4/8` parsed with `invalid_count = 4`.
- Allowed-set multi-GPU verification is now also present:
  - `run-20260311T061434Z-10e36149` on GPUs `5,6`
- GPU6 strict-final follow-up is also present:
  - `run-20260311T063838Z-7956de92`
- AIME GPU7 offline smoke is also present:
  - `run-20260311T064335Z-1ab1abe2`

## Open questions

1. Can we improve final-answer emission without sacrificing the better accuracy of the non-strict parserfix run?
2. Should local snapshot-path model runs be normalized back to canonical model naming in scoreboard reporting?
3. Which follow-up dataset after GPQA should get the next `5,6,7` continuation slot: GSM8K or MMLU?
