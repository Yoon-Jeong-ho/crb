# RESULTS LOG

- Date: 2026-03-11
- Current continuation team: `crb-gpu567-continuation-gpus-5`
- Current GPU rule: `5,6,7 only`

## Carry-over verified evidence

- Earlier today, GPQA / Qwen3 thinking-off smoke was re-verified on **GPU 4** and recorded as bootstrap baseline evidence.
  - `run-20260311T053304Z-f40cce6c`
  - `run-20260311T054045Z-c4316b30`
- These runs remain valid reference points for the day, but they are **carry-over evidence**, not new GPU567-cycle launches.

## First true GPU567-cycle result

- GPQA / Qwen3 thinking-on / parserfix smoke succeeded on **GPU 5**.
  - config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix.yaml`
  - run id: `run-20260311T060823Z-1947f5cf`
  - accuracy: `0.375`
  - format failure rate: `0.5`
  - parsed_count: `4`
  - invalid_count: `4`
  - JSON: `Legacy/results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix__1947f5cf9df42ec1/run-20260311T060823Z-1947f5cf.json`
  - log: `Legacy/logs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix__1947f5cf9df42ec1.log`
  - scoreboard: appended in `Legacy/results/summary/scoreboard.csv`

## Current continuation status

- The GPU567 branch now has its first verified run.
- The parserfix branch is no longer purely hypothetical, but `format_failure_rate = 0.5` means more work is still required.

## Additional GPU567-cycle verification

- GPQA / Qwen3 thinking-off / multi-GPU smoke succeeded on **GPUs 5,6**.
  - config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_multigpu_gpu56_smoke_20260311.yaml`
  - run id: `run-20260311T061434Z-10e36149`
  - accuracy: `0.5`
  - format failure rate: `0.0`
  - parsed_count: `2`
  - invalid_count: `0`
  - JSON: `Legacy/results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_multigpu_gpu56_smoke_20260311__10e361496f9e67c7/run-20260311T061434Z-10e36149.json`
  - scoreboard: appended in `Legacy/results/summary/scoreboard.csv`

## Current interpretation

- Allowed GPU set `5,6,7` 기준으로:
  - single-GPU continuation evidence: 확보
  - multi-GPU continuation evidence: 확보
- 남은 핵심 문제는 **thinking-on parserfix branch의 invalid 4건**이다.

## Already pushed documentation baseline

- `28e4058` — bootstrap root bridge + GPU4 smoke rerun logging
- `02fa431` — pushed bootstrap status capture

## Next expected entries

1. Invalid-output review for `run-20260311T060823Z-1947f5cf`
2. GPU 6 or 7 follow-up parserfix rerun
3. If needed, stricter final-answer prompt or decoding adjustment
