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

## GPU6 follow-up rerun

- GPQA / Qwen3 thinking-on / parserfix + strictfinal follow-up ran on **GPU 6**.
  - config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix_gpu6_strictfinal_20260311.yaml`
  - run id: `run-20260311T063838Z-7956de92`
  - accuracy: `0.125`
  - format failure rate: `0.375`
  - parsed_count: `5`
  - invalid_count: `3`
- interpretation:
  - strict-final prompt reduced invalids (`4 -> 3`)
  - but hurt accuracy (`0.375 -> 0.125`)
  - so this is not yet the replacement thinking-on baseline

## AIME refresh

- AIME / Qwen3 thinking-off / offline smoke succeeded on **GPU 7**.
  - config: `Legacy/configs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off_gpu7_offline_smoke_20260311.yaml`
  - run id: `run-20260311T064335Z-1ab1abe2`
  - accuracy: `0.125`
  - format failure rate: `0.25`
  - parsed_count: `6`
  - invalid_count: `2`
  - JSON: `Legacy/results/runs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off_gpu7_offline_smoke_20260311__1ab1abe2aef754b4/run-20260311T064335Z-1ab1abe2.json`

## Already pushed documentation baseline

- `28e4058` — bootstrap root bridge + GPU4 smoke rerun logging
- `02fa431` — pushed bootstrap status capture

## Next expected entries

1. Choose the next thinking-on branch:
   - keep parserfix base prompt, or
   - keep strict-final prompt but recover accuracy
2. Tune final-answer emission / decoding
3. If needed, add one GSM8K or MMLU continuation rerun
