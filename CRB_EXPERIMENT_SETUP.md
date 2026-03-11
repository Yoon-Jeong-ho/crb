# CRB Experiment Setup

## 0. Continuation snapshot (2026-03-11)

- active team: `crb-gpu567-continuation-gpus-5`
- runnable tree: `Legacy/`
  - code: `Legacy/src/crb`
  - configs: `Legacy/configs`
  - tests: `Legacy/tests`
  - outputs: `Legacy/results`, `Legacy/logs`
- env: `/data_x/aa007878/projects/crb/.conda/envs/crb`
- **GPU rule for this continuation pass: `5,6,7 only`**
- carry-over reference only: earlier GPU4 GPQA smoke reruns from the same day
- already pushed baseline commits: `28e4058`, `02fa431`
- current continuation cycle now has:
  - one verified GPU5 parserfix smoke,
  - one verified GPU6 strict-final follow-up,
  - one verified GPUs 5,6 multi-GPU smoke,
  - one verified GPU7 AIME offline smoke

## 1. Goal

- single-turn benchmark를 multi-turn accumulated-history 평가로 바꿨을 때 성능 저하/간섭을 측정한다.
- 이번 continuation pass의 실질 목표는:
  1. thinking-off baseline을 historical reference로 유지하고,
  2. thinking-on parser/postprocessing 병목을 parserfix branch로 줄여 보고,
  3. 새 evidence를 `5/6/7` 범위 GPU에서만 추가하는 것이다.

## 2. Current run rules

- 새 env를 만들지 않는다.
- 새 코드/설정의 실제 실행은 `cd Legacy` + `PYTHONPATH=src` 기준으로 한다.
- 이번 run에서는 GPU `5,6,7`만 사용한다.
- GPU4 결과는 **오늘 확보된 baseline evidence**로만 남기고, 새 continuation launch에는 재사용하지 않는다.
- parserfix는 첫 smoke가 검증됐지만, 아직 추가 rerun과 invalid-case 정리가 필요하다.

## 3. Fresh verified result

- GPU 5 / GPQA / Qwen3 thinking-on / parserfix smoke
  - config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix.yaml`
  - run id: `run-20260311T060823Z-1947f5cf`
  - num_items: `8`
  - accuracy: `0.375`
  - format_failure_rate: `0.5`
  - parsed_count / invalid_count: `4 / 4`
  - evidence:
    - JSON: `Legacy/results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix__1947f5cf9df42ec1/run-20260311T060823Z-1947f5cf.json`
    - log: `Legacy/logs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix__1947f5cf9df42ec1.log`
    - scoreboard: `Legacy/results/summary/scoreboard.csv`

- GPU 5,6 / GPQA / Qwen3 thinking-off / multi-GPU smoke
  - config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_multigpu_gpu56_smoke_20260311.yaml`
  - run id: `run-20260311T061434Z-10e36149`
  - num_items: `2`
  - accuracy: `0.5`
  - format_failure_rate: `0.0`
  - parsed_count / invalid_count: `2 / 0`
  - evidence:
    - JSON: `Legacy/results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_multigpu_gpu56_smoke_20260311__10e361496f9e67c7/run-20260311T061434Z-10e36149.json`
    - scoreboard: `Legacy/results/summary/scoreboard.csv`

- GPU 6 / GPQA / Qwen3 thinking-on / parserfix + strictfinal follow-up
  - config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix_gpu6_strictfinal_20260311.yaml`
  - run id: `run-20260311T063838Z-7956de92`
  - num_items: `8`
  - accuracy: `0.125`
  - format_failure_rate: `0.375`
  - parsed_count / invalid_count: `5 / 3`

- GPU 7 / AIME / Qwen3 thinking-off / offline smoke
  - config: `Legacy/configs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off_gpu7_offline_smoke_20260311.yaml`
  - run id: `run-20260311T064335Z-1ab1abe2`
  - num_items: `8`
  - accuracy: `0.125`
  - format_failure_rate: `0.25`
  - parsed_count / invalid_count: `6 / 2`

## 4. Immediate experiment checklist

- [x] GPU 5에서 GPQA thinking-on parserfix smoke 1회
- [x] 첫 true GPU567-cycle result를 문서화
- [x] allowed subset `5,6`으로 multi-GPU smoke 1회
- [x] invalid 4건 원인 확인
- [x] GPU 6 또는 7에서 follow-up single-GPU rerun 1회
- [x] AIME fresh numeric rerun 1회

## 5. Output locations

- run JSON / partials: `Legacy/results/runs/`
- manifests: `Legacy/results/manifests/`
- scoreboard: `Legacy/results/summary/scoreboard.csv`
- logs: `Legacy/logs/`

## 6. Notes

- `README_CRB.md`와 older 문서는 current continuation GPU rule과 다를 수 있으므로 historical 참고로만 본다.
- 더 긴 기존 setup/spec 문서는 `docs/CRB_EXPERIMENT_SETUP_LONGFORM_ARCHIVE_20260311.md`에 보존했다.
- parserfix 관련 코드/config는 아직 로컬 변경 상태이므로, 새 push 전까지는 `main` 기준 stable reference를 함께 본다.
- 현재 판단:
  - parser regex 보강은 유지할 가치가 있다.
  - strict-final prompt는 형식엔 도움이 있지만 정확도를 깎는다.
  - 다음 개선 포인트는 **final-answer emission / decoding** 쪽이다.
