# CRB Bootstrap Workspace

CRB(Conversation-Accumulated Robustness Benchmark)는 single-turn benchmark를 **multi-turn accumulated history** 환경으로 바꿔, 앞선 더미 턴이 마지막 실제 평가 문제 성능을 얼마나 흔드는지 확인하는 작업공간입니다.

현재 연구의 primary focus는:
- 앞의 **k개 dummy turns** 가 마지막 target를 얼마나 흔드는지
- `multi_turn vs flattened`
- `self_history vs oracle_history`
- `same_domain vs cross_domain`
를 채우는 것이다.

`thinking on/off`는 이 메커니즘을 읽는 **secondary axis** 로 취급한다.

## Current continuation snapshot (2026-03-11)

- 팀: `crb-gpu567-continuation-gpus-5`
- 실제 runnable code/config/tests/results 트리는 여전히 `Legacy/` 아래에 있습니다.
- 루트는 현재 **bootstrap 문서 + 실행 가이드 + 팀 조율용 레이어**입니다.
- 사용 env: `/data_x/aa007878/projects/crb/.conda/envs/crb`
- **이번 continuation run의 GPU 규칙은 `5,6,7 only`** 입니다.
- 2026-03-11 저녁 follow-up sweep은 **실제 가용 GPU가 `5,6`뿐이어서 그 두 장만 사용**했습니다.
- 오늘 earlier에 확보한 GPU4 smoke evidence는 **carry-over baseline**으로만 취급합니다. 새 launch는 5/6/7에서만 진행합니다.

## Already pushed

- `28e4058` — bootstrap root bridge + GPQA GPU4 smoke rerun 기록
- `02fa431` — pushed bootstrap status 문서 반영
- 현재 `main == origin/main` 입니다. 즉, 위 두 커밋은 이미 원격 기준선입니다.

## Fresh verified continuation result

- GPQA / Qwen3 thinking-on parserfix smoke가 **GPU 5**에서 성공했습니다.
  - config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix.yaml`
  - run id: `run-20260311T060823Z-1947f5cf`
  - accuracy: `0.375`
  - format failure rate: `0.5`
  - parsed / invalid: `4 / 4`
- 해석: parserfix 경로가 첫 GPU567-cycle run은 만들었지만, 아직 절반이 invalid라 추가 정리가 필요합니다.

## Fresh verified multi-GPU result

- GPQA / Qwen3 thinking-off multi-GPU smoke가 **GPU 5,6**에서 성공했습니다.
  - config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_multigpu_gpu56_smoke_20260311.yaml`
  - run id: `run-20260311T061434Z-10e36149`
  - accuracy: `0.5`
  - format failure rate: `0.0`
  - parsed / invalid: `2 / 0`
- 해석: continuation cycle 안에서 allowed GPU set 기준의 single-GPU + multi-GPU evidence를 둘 다 확보했습니다.

## Additional continuation evidence

- GPU 6 / GPQA / thinking-on parserfix + strictfinal follow-up
  - run: `run-20260311T063838Z-7956de92`
  - accuracy `0.125`
  - format failure `0.375`
  - 해석: 형식은 조금 나아졌지만 정확도는 악화되어, 현재 active thinking-on path로 채택하기 어렵습니다.
- GPU 7 / AIME / thinking-off offline smoke
  - run: `run-20260311T064335Z-1ab1abe2`
  - accuracy `0.125`
  - format failure `0.25`

## Fresh GPU5/6 follow-up sweep

- GPU 5,6 / GPQA / thinking-on / **choice constrained only**
  - run: `run-20260311T091942Z-f3e9f0fa`
  - accuracy `0.25`
  - format failure `0.0`
  - parsed / invalid `8 / 0`
  - 해석: 형식은 완전히 안정화됐지만, 출력이 사실상 전부 `A`로 붕괴해 정확도가 떨어졌습니다.
- GPU 5,6 / GPQA / thinking-on / **`/no_think` + prefill**
  - run: `run-20260311T092221Z-dfa04164`
  - accuracy `0.375`
  - format failure `0.0`
  - parsed / invalid `8 / 0`
- GPU 5,6 / GPQA / thinking-on / **choice constrained + `/no_think` + prefill**
  - run: `run-20260311T092432Z-dac259a0`
  - accuracy `0.375`
  - format failure `0.0`
  - parsed / invalid `8 / 0`
- 해석:
  - `/no_think` + prefill 계열은 parserfix baseline의 정확도(`0.375`)를 유지하면서 invalid를 `4 -> 0`으로 줄였습니다.
  - combined config도 같은 정확도를 냈지만, **단순성 기준의 현재 winner는 `/no_think` + prefill 단독안**입니다.

## Current parserfix branch files

- parserfix 작업 파일:
  - `Legacy/src/crb/evaluation/parsers.py`
  - `Legacy/tests/test_parsers.py`
  - `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix.yaml`
- 현재 상태:
  - GPU5 parserfix smoke 검증 완료
  - GPU6 strict-final follow-up 검증 완료
  - GPU5/6 follow-up sweep까지 반영하면, parser 추가보다 **target turn final-answer emission 제어**가 더 효과적임이 확인됐습니다.

## Operational reality

- 실행은 당분간 `cd Legacy` 후 `PYTHONPATH=src` 기준으로 진행합니다.
- 결과물은 `Legacy/results/` 와 `Legacy/logs/` 아래에 쌓입니다.
- 시작 문서:
  - 운영 가이드: `CRB_EXPERIMENT_SETUP.md`
  - 이전 장문 연구/운영 스펙 아카이브: `docs/CRB_EXPERIMENT_SETUP_LONGFORM_ARCHIVE_20260311.md`
  - 리서치 노트: `research/README.md`
  - 현재 상태: `docs/EXECUTION_STATUS.md`
  - 결과 로그: `docs/RESULTS_LOG.md`
  - 해석: `docs/ANALYSIS.md`
  - 다음 액션: `docs/TODO_NEXT.md`

## Next actions

1. `k={0,2,4,8}` 와 `mode/history/domain` 축을 채우는 broader sweep을 계속 진행합니다.
2. accumulated-history mechanism rows를 먼저 확보하고, 그 위에서 thinking on/off 차이를 읽습니다.
3. GPQA thinking-on rescue config (`/no_think` + prefill)는 유지하되, 전체 연구 narrative의 중심에 두지 않습니다.

## Research-backed next bets

- Qwen 공식 문서는 thinking mode에서 `temperature=0.6`, `top_p=0.95`, `top_k=20`을 권장하고, overly greedy한 설정은 반복/품질 저하를 부를 수 있다고 안내합니다.
- Qwen 공식 문서는 turn-level 제어로 `/think`, `/no_think`, 또는 assistant prefill `<think>\n\n</think>\n\n` 패턴을 제공합니다.
- vLLM 공식 문서는 structured outputs의 `choice` / `regex` 제약을 지원합니다.
- 따라서 지금 가장 유망한 다음 개선은:
  1. `k / mode / history / domain` 축을 우선 채우는 것
  2. target turn emission control은 GPQA thinking-on rescue용 보조 수단으로만 쓰는 것
  3. **choice-only constrained decoding은 단독으로 쓰지 않는 것** (2026-03-11 follow-up에서 all-`A` 붕괴 확인)
