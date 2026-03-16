# CRB Analysis Workspace

이 폴더는 `Legacy/results/summary/scoreboard.csv` 와 `Legacy/results/runs/**/*.json` 을 읽어,
루트 레벨에서 재사용 가능한 분석 산출물을 정리하는 곳입니다.

## Layout
- `methods.md` — 현재 권장 분석 방법과 입력/출력 정의
- `types.md` — 어떤 분석을 어떤 질문에 쓰는지 정리한 분류표
- `generated/` — CSV / JSON 집계 결과
- `plots/` — SVG 시각화 결과

## Default workflow
1. `python -m tools.aggregate_results`
2. `python -m tools.build_tables`
3. `python -m tools.bucket_errors`
4. `python -m tools.plot_results`
5. `docs/OPERATOR_NEXT_STEPS.md` 체크리스트로 다음 의사결정 정리

## Ground rules
- 새 실험은 여기서 돌리지 않습니다.
- 실행 가능한 평가 코드는 계속 `Legacy/` 아래에 둡니다.
- results/logs 원본은 계속 `Legacy/results`, `Legacy/logs` 를 source of truth로 사용합니다.
