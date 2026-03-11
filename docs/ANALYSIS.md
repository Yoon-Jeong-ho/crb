# ANALYSIS

- Date: 2026-03-11

## Bootstrap conclusions

1. **`Legacy/`가 현재 유일한 runnable CRB 파이프라인이다.**
   - 루트에는 `src/`, `configs/`, `tests/`, `scripts/`가 없다.
   - 실제 실행/검증은 `Legacy/src/crb`, `Legacy/configs`, `Legacy/tests` 기준으로 이뤄져야 한다.
2. **루트는 당분간 “rewrite 대상”이 아니라 “wrapper / bootstrap shell”로 다루는 편이 안전하다.**
   - 빈 `README.md`를 채우고,
   - 루트 문서에서 `Legacy/`를 현재 실행 경로로 명시하고,
   - promote-vs-wrap 결정을 별도 단계로 두는 것이 가장 리스크가 낮다.
3. **문서 정책은 이제 GPUs `4,5,6,7 only`로 통일되어야 한다.**
   - 기존 `README_CRB.md`와 일부 setup 문서는 `6,7` 중심이라 현재 운영 규칙과 어긋난다.

## Verified legacy evidence to carry forward

- GPQA / Qwen3 thinking off
  - smoke: accuracy `0.500`, format failure `0.000`
  - mini: accuracy `0.40625`, format failure `0.000`
  - 해석: baseline path로 가장 안정적이다.
- GPQA / Qwen3 thinking on
  - smoke: accuracy `0.125`, format failure `0.875`
  - strict-final rescue: accuracy `0.000`, format failure `1.000`
  - 해석: 현재 병목은 정답 품질보다 **format / postprocessing collapse**에 가깝다.
- GSM8K / Qwen3 off/on pair
  - off: accuracy `0.375`, format failure `0.250`
  - on: accuracy `0.125`, format failure `0.125`
  - 해석: thinking-on 문제가 GPQA처럼 전역적으로 터지는 것은 아니다.
- AIME / Qwen3 thinking off
  - smoke/mini 모두 accuracy `0.125`, format failure `0.250`
  - 해석: numeric evaluator path는 살아 있고, 남은 문제는 품질/모호성이다.

## New bootstrap-cycle smoke evidence

- 2026-03-11에 worker-5가 **GPU 4**에서 GPQA thinking-off smoke를 새로 실행했다.
- 실행 위치: `Legacy/`
- 핵심 조건:
  - model: `Qwen/Qwen3-1.7B`
  - dataset: `gpqa`
  - mode: `multi_turn`
  - history: `oracle_history`
  - dummy: `same_domain`
  - `k=2`, `num_items=8`
- 결과:
  - run id: `run-20260311T054045Z-c4316b30`
  - accuracy `0.500`
  - format failure `0.000`
  - scoreboard append 확인
- 산출물:
  - JSON: `Legacy/results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_gpu4_worker5_smoke_20260311__c4316b30556d7ecf/run-20260311T054045Z-c4316b30.json`
  - log: `Legacy/logs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_gpu4_worker5_smoke_20260311__c4316b30556d7ecf.log`

## Operational lesson from the smoke rerun

- 첫 sandboxed 시도는 Hugging Face 접근이 막혀 `ConnectionError`로 실패했다.
- unsandboxed 재시도로 dataset download 후 정상 실행되었다.
- 추론: 새 머신/새 캐시 상황의 smoke 검증은 **로컬 코드만 있어도 외부 dataset 접근**이 필요할 수 있다.

## What this means next

- 가장 빠른 안전 경로는 **Legacy를 즉시 재작성하는 것보다, 루트 README/docs를 Legacy 실행 경로에 맞게 정렬하는 것**이다.
- 다음 진짜 기술 병목은:
  1. root package/layout 정렬,
  2. GPQA thinking-on parser/postprocessing 개선,
  3. selective sweep 운영이다.
