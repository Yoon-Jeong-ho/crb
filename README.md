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

## Local work in progress (not pushed yet)

- parserfix 작업 파일:
  - `Legacy/src/crb/evaluation/parsers.py`
  - `Legacy/tests/test_parsers.py`
  - `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_parserfix.yaml`
- 현재 상태: **GPU5 smoke 1회는 검증됨**, 하지만 코드는 아직 로컬 변경 상태이며 추가 rerun/정리가 남아 있습니다.

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

1. `run-20260311T060823Z-1947f5cf`의 invalid 4건을 확인합니다.
2. 현재 invalid가 parser regex 문제인지, **final answer 미출력/생성 truncation**인지 분리합니다.
3. **GPU 6 또는 7**에서 parserfix follow-up single-GPU rerun을 1회 더 남깁니다.
4. 새 결과가 생기면 `docs/RESULTS_LOG.md` / `docs/ANALYSIS.md` / `docs/TODO_NEXT.md`를 즉시 동기화합니다.
