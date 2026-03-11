# CRB Bootstrap Workspace

CRB(Conversation-Accumulated Robustness Benchmark)는 single-turn benchmark를 **multi-turn accumulated history** 환경으로 바꿔, 앞선 더미 턴이 마지막 실제 평가 문제의 성능을 얼마나 흔드는지 측정하는 실험 작업공간입니다.

## Current reality (2026-03-11)

- 현재 **실제로 실행되는 코드/config/tests/results 트리**는 `Legacy/` 아래에 있습니다.
- 루트는 지금 **bootstrap 문서 + 팀 조율용 셸** 역할을 합니다.
- 현재 사용 가능한 env는 `/data_x/aa007878/projects/crb/.conda/envs/crb` 하나뿐입니다.
- 이번 사이클 GPU 정책은 **`4,5,6,7`만 사용**입니다.
- 루트 `pyproject.toml`과 실제 코드 위치는 아직 정렬되지 않았습니다.

## What is already verified

- `Legacy/`에는 Qwen3 기반 GPQA / GSM8K / AIME smoke·mini run 결과가 이미 있습니다.
- GPQA thinking off 경로는 smoke/mini 기준으로 가장 안정적인 baseline입니다.
- GSM8K는 thinking off/on 직접 비교 pair가 있습니다.
- AIME는 numeric parser/evaluator 경로가 검증되어 벤치마크 축으로 유지 가능합니다.

## Recommended starting points

- 실험 설계 / 운영 원칙: `CRB_EXPERIMENT_SETUP.md`
- 현재 부트스트랩 상태: `docs/EXECUTION_STATUS.md`
- 핵심 해석: `docs/ANALYSIS.md`
- 다음 우선순위: `docs/TODO_NEXT.md`
- 이전 개요 문서(역사적 참고): `README_CRB.md`
- 현재 실행 가능한 파이프라인 문서: `Legacy/README.md`

## Run the currently verified pipeline

현재 기준으로는 루트가 아니라 `Legacy/`에서 실행해야 합니다.

```bash
cd /data_x/aa007878/projects/crb/Legacy
HF_HOME=/mnt/raid6/aa007878/.cache/huggingface \
PYTHONNOUSERSITE=1 \
PYTHONPATH=src \
CUDA_VISIBLE_DEVICES=4 \
/data_x/aa007878/projects/crb/.conda/envs/crb/bin/python \
  -m crb.cli.run_eval \
  --config configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off.yaml
```

### Output locations

- run JSON / partials: `Legacy/results/runs/`
- manifests: `Legacy/results/manifests/`
- scoreboard: `Legacy/results/summary/scoreboard.csv`
- logs: `Legacy/logs/`

## Notes

- `README_CRB.md`의 실행 예시는 현재보다 오래된 `6,7` GPU 규칙을 포함하므로, **개념 참고용**으로만 보세요.
- 루트 정렬이 끝나기 전까지는 **Legacy 삭제 금지**가 기본 원칙입니다.
