# CRB Analysis Workspace

이 폴더는 현재 **legacy-derived analysis 산출물 중심**이다.

주요 입력은 아직:

- `Legacy/results/summary/scoreboard.csv`
- `Legacy/results/runs/**/*.json`

이다.

## Current status

- `analysis/`는 기존 논문 story용 legacy artifact 분석에 계속 유효하다.
- 새 `crb_v2` 실행 결과의 기본 집계는 우선 각 run root의 `aggregate/` 아래에서 읽는 것이 맞다.
- 즉:
  - legacy slice analysis → `analysis/`
  - new v2 run summary → `results_v2/<experiment>__<hash>/aggregate/`

## Default workflow for legacy analysis

1. `python -m tools.aggregate_results`
2. `python -m tools.build_tables`
3. `python -m tools.bucket_errors`
4. `python -m tools.plot_results`
5. `docs/TODO_NEXT.md` 에 다음 의사결정 반영

## Ground rules

- 새 실험은 여기서 돌리지 않는다.
- 새 실행 코드는 `src/crb_v2/` + `configs_v2/` 를 사용한다.
- `Legacy/results` 는 legacy source of truth이다.
- `results_v2` 는 v2 source of truth이다.
