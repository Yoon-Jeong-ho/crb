# CRB Bootstrap Workspace

CRB(Conversation-Accumulated Robustness Benchmark)는 single-turn benchmark를 **multi-turn accumulated history** 환경으로 바꿔, 앞선 더미 턴이 마지막 실제 평가 문제 성능을 얼마나 흔드는지 확인하는 작업공간입니다.

## Current continuation snapshot (2026-03-11)

- 팀: `crb-gpu567-continuation-gpus-5`
- 실제 runnable code/config/tests/results 트리는 여전히 `Legacy/` 아래에 있습니다.
- 루트는 현재 **bootstrap 문서 + 실행 가이드 + 팀 조율용 레이어**입니다.
- 사용 env: `/data_x/aa007878/projects/crb/.conda/envs/crb`
- **이번 continuation run의 GPU 규칙은 `5,6,7 only`** 입니다.
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

## Current parserfix branch files

- parserfix 작업 파일:
  - `Legacy/src/crb/evaluation/parsers.py`
  - `Legacy/tests/test_parsers.py`
  - `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix.yaml`
- 현재 상태:
  - GPU5 parserfix smoke 검증 완료
  - GPU6 strict-final follow-up 검증 완료
  - 여전히 next step은 parser 추가보다 **final-answer emission / decoding 보정**입니다.

## Operational reality

- 실행은 당분간 `cd Legacy` 후 `PYTHONPATH=src` 기준으로 진행합니다.
- 결과물은 `Legacy/results/` 와 `Legacy/logs/` 아래에 쌓입니다.
- 시작 문서:
  - 운영 가이드: `CRB_EXPERIMENT_SETUP.md`
  - 이전 장문 연구/운영 스펙 아카이브: `docs/CRB_EXPERIMENT_SETUP_LONGFORM_ARCHIVE_20260311.md`
  - 현재 상태: `docs/EXECUTION_STATUS.md`
  - 결과 로그: `docs/RESULTS_LOG.md`
  - 해석: `docs/ANALYSIS.md`
  - 다음 액션: `docs/TODO_NEXT.md`

## Next actions

1. thinking-on branch에서 **final answer emission**을 개선할 다음 config를 정합니다.
2. GSM8K 또는 MMLU 중 다음 `5,6,7` continuation slot을 선택합니다.
3. 새 결과가 생기면 `docs/RESULTS_LOG.md` / `docs/ANALYSIS.md` / `docs/TODO_NEXT.md`를 즉시 동기화합니다.
