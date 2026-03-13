# EXECUTION STATUS

- Date: 2026-03-11
- Team: `crb-gpu567-continuation-gpus-5`
- Basis docs: `README.md`, `CRB_EXPERIMENT_SETUP.md`, `docs/RESULTS_LOG.md`, `docs/ANALYSIS.md`, `docs/TODO_NEXT.md`
- Env: `/data_x/aa007878/projects/crb/.conda/envs/crb`
- GPU rule for **this continuation run**: `5,6,7` only
- 2026-03-11 저녁 follow-up slot actual GPU availability: `5,6` only

## Current state

- [x] Root vs `Legacy/` runnable split re-confirmed
- [x] Docs refreshed for the GPU567 continuation pass
- [x] Earlier pushed baseline commits recorded: `28e4058`, `02fa431`
- [x] Historical GPQA thinking-off GPU4 smoke evidence carried forward as reference
- [x] Parserfix branch validated with a fresh GPU5 run
- [x] First true continuation-cycle result logged
- [x] One allowed multi-GPU verification completed on GPUs `5,6`
- [x] Parserfix follow-up rerun on GPU6 logged
- [x] Remaining invalid outputs analyzed
- [x] AIME refresh on GPU7 logged
- [x] GPQA choice-only follow-up on GPUs `5,6` logged
- [x] GPQA `/no_think` + prefill follow-up on GPUs `5,6` logged
- [x] GPQA combined follow-up on GPUs `5,6` logged

## Fresh verified result

- experiment: GPQA / Qwen3 thinking-on / parserfix smoke
- GPU: `5`
- config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix.yaml`
- run id: `run-20260311T060823Z-1947f5cf`
- metrics:
  - accuracy `0.375`
  - format failure `0.500`
  - parsed `4/8`
  - invalid `4/8`
- evidence:
  - JSON: `Legacy/results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix__1947f5cf9df42ec1/run-20260311T060823Z-1947f5cf.json`
  - log: `Legacy/logs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix__1947f5cf9df42ec1.log`
  - scoreboard append confirmed in `Legacy/results/summary/scoreboard.csv`

## Fresh multi-GPU verification

- experiment: GPQA / Qwen3 thinking-off / multi-GPU smoke
- GPUs: `5,6`
- config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_multigpu_gpu56_smoke_20260311.yaml`
- run id: `run-20260311T061434Z-10e36149`
- metrics:
  - accuracy `0.500`
  - format failure `0.000`
  - parsed `2/2`
  - invalid `0/2`
- evidence:
  - JSON: `Legacy/results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_multigpu_gpu56_smoke_20260311__10e361496f9e67c7/run-20260311T061434Z-10e36149.json`
  - scoreboard row: `Legacy/results/summary/scoreboard.csv`

## Follow-up single-GPU rerun

- experiment: GPQA / Qwen3 thinking-on / parserfix + strictfinal
- GPU: `6`
- config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix_gpu6_strictfinal_20260311.yaml`
- run id: `run-20260311T063838Z-7956de92`
- metrics:
  - accuracy `0.125`
  - format failure `0.375`
  - parsed `5/8`
  - invalid `3/8`
- interpretation:
  - format failure improved vs GPU5 parserfix run
  - accuracy got worse
  - branch is still not ready to call stable

## AIME refresh

- experiment: AIME / Qwen3 thinking-off / offline smoke
- GPU: `7`
- config: `Legacy/configs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off_gpu7_offline_smoke_20260311.yaml`
- run id: `run-20260311T064335Z-1ab1abe2`
- metrics:
  - accuracy `0.125`
  - format failure `0.250`
  - parsed `6/8`
  - invalid `2/8`

## GPU5/6 follow-up sweep

- experiment: GPQA / Qwen3 thinking-on / choice constrained only
  - GPUs: `5,6`
  - config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_choiceconstrained.yaml`
  - run id: `run-20260311T091942Z-f3e9f0fa`
  - metrics:
    - accuracy `0.250`
    - format failure `0.000`
    - parsed `8/8`
    - invalid `0/8`
  - interpretation:
    - formatting failure는 사라졌지만,
    - 모델이 사실상 `A`로 붕괴해 active winner로 채택하기 어렵다.

- experiment: GPQA / Qwen3 thinking-on / `/no_think` + prefill
  - GPUs: `5,6`
  - config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_nothink_prefill.yaml`
  - run id: `run-20260311T092221Z-dfa04164`
  - metrics:
    - accuracy `0.375`
    - format failure `0.000`
    - parsed `8/8`
    - invalid `0/8`

- experiment: GPQA / Qwen3 thinking-on / choice constrained + `/no_think` + prefill
  - GPUs: `5,6`
  - config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_choiceconstrained_nothink_prefill.yaml`
  - run id: `run-20260311T092432Z-dac259a0`
  - metrics:
    - accuracy `0.375`
    - format failure `0.000`
    - parsed `8/8`
    - invalid `0/8`

## Current winner

- `/no_think` + prefill이 현재 가장 실용적인 winner다.
  - parserfix baseline accuracy(`0.375`)를 유지했다.
  - format failure를 `0.5 -> 0.0`으로 낮췄다.
  - combined config와 정확도는 같지만, 추가 제약이 적어 더 단순하다.
- combined config는 출력 surface가 더 깔끔한 fallback 후보로는 남길 가치가 있다.

## Current parserfix branch files

- parserfix files currently present locally:
  - `Legacy/src/crb/evaluation/parsers.py`
  - `Legacy/tests/test_parsers.py`
  - `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix.yaml`
- meaning:
  - parser regex improvement itself is worth keeping
  - 기존 remaining failures는 mostly no-final-answer / truncation이었다
  - follow-up sweep 결과, next change target은 parser 확장이 아니라 **target-turn control 선택과 재현성 확인**이다

## Immediate queue

1. `/no_think` + prefill을 active thinking-on follow-up baseline으로 확정할지 결정한다.
2. combined config를 fallback으로 유지할지 정한다.
3. GSM8K 또는 MMLU 중 어느 dataset에 winning control을 먼저 이식할지 정한다.

## Risks / blockers

- parserfix 자체는 더 이상 unverified가 아니지만, 이제 active decision point는 “어느 control을 기본값으로 채택할지”이다.
- 새로운 follow-up 3개는 모두 `n=8` 결과라서 추가 rerun 없이 과신하면 안 된다.
- choice-only constrained decoding은 all-`A` collapse risk를 드러냈다.
- GPU4 smoke evidence remains helpful baseline material, not the scheduler rule for this continuation pass.
- Root package/layout mismatch still exists; docs are aligned first, code/package cleanup remains separate work.
