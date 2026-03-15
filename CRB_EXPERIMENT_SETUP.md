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
  - one verified GPU7 AIME offline smoke,
  - one verified GPU5/6 choice-only follow-up,
  - one verified GPU5/6 `/no_think` + prefill follow-up,
  - one verified GPU5/6 combined follow-up

## 1. Goal

- single-turn benchmark를 multi-turn accumulated-history 평가로 바꿨을 때 성능 저하/간섭을 측정한다.
- 이번 continuation pass의 실질 목표는:
  1. **앞의 k개 dummy turn** 이 마지막 target를 얼마나 흔드는지 보는 CRB protocol을 먼저 채우고,
  2. `multi_turn vs flattened`, `self_history vs oracle_history`, `same_domain vs cross_domain`, `k={0,2,4,8}` 축을 메인 분석 대상으로 유지하며,
  3. thinking on/off는 이 accumulated-interference 결과를 읽는 **secondary axis** 로 다루는 것이다.

## 2. Current run rules

- 새 env를 만들지 않는다.
- 새 코드/설정의 실제 실행은 `cd Legacy` + `PYTHONPATH=src` 기준으로 한다.
- 이번 run에서는 GPU `5,6,7`만 사용한다.
- GPU4 결과는 **오늘 확보된 baseline evidence**로만 남기고, 새 continuation launch에는 재사용하지 않는다.
- parserfix는 첫 smoke가 검증됐지만, 아직 추가 rerun과 invalid-case 정리가 필요하다.
- 2026-03-11 저녁 follow-up은 가용성 제약 때문에 GPU `5,6`만 사용한다.

## 2.1 How `k` dummy turns are inserted right now

- 구현 위치
  - manifest sampling: `Legacy/src/crb/sampling/dummy_sampler.py`
  - runtime insertion: `Legacy/src/crb/evaluation/runner.py`
- 현재 방식은 **target item마다 미리 reproducible dummy list를 만들고**, 실제 run에서는 그 prefix를 잘라 쓴다.
- 구체적으로는:
  1. 각 target item마다 `same_domain` / `cross_domain` 후보 dummy를 미리 만든다.
  2. 후보는 `max(manifest_k_values)` 개까지 뽑는다.
  3. 실제 run에서는 `dummy_ids_by_type[dummy_type][:k]` 를 사용한다.
  4. 즉, `k=2` 는 `k=4` 와 `k=8` 의 **prefix subset** 이다.
- 이 prefix 구조의 장점
  - `k` 증가 효과를 비교할 때 sample composition drift가 줄어든다.
  - 같은 target에 대해 `k=2 -> 4 -> 8` 비교가 더 해석 가능해진다.

### same_domain / cross_domain 판정

- `same_domain`
  - normalized `subject` 가 같거나
  - normalized `domain` 이 같으면 허용
  - 둘 다 없으면 같은 dataset으로 fallback
- `cross_domain`
  - normalized `subject` / `domain` 이 둘 다 다르면 허용
  - 둘 다 없으면 다른 dataset으로 fallback

### history_mode에 따른 삽입 차이

- `oracle_history`
  - dummy turn answer를 gold canonical answer로 바로 넣는다.
  - dummy generation step이 없다.
- `self_history`
  - dummy 1을 생성하고 history에 넣고,
  - 그 상태에서 dummy 2를 생성하고,
  - 이런 식으로 **sequentially accumulated** 된다.
  - 따라서 `self_history` 는 단순 length 증가가 아니라 **model’s own prior answers contamination** 을 포함한다.

### evaluation_mode에 따른 삽입 차이

- `multi_turn`
  - history를 실제 `user` / `assistant` turn으로 번갈아 넣고
  - 마지막에 target question user turn을 붙인다.
- `single_turn_flattened`
  - history를 `[History i]` 블록으로 평탄화하고
  - 마지막 target question을 이어 붙인다.
- 따라서 `multi_turn vs flattened` 는 token length보다 **turn structure effect** 를 보기 위한 비교다.

### scoring rule

- 앞의 `k` dummy는 채점하지 않는다.
- **마지막 target answer만 채점** 한다.
- 이 점이 CRB의 핵심이다.

## 2.2 Other viable choices worth considering

- 유지할 가치가 큰 현재 선택
  - prefix-based `k` sampling
  - target-only scoring
  - `self_history` vs `oracle_history`
  - explicit `wrong_history`
  - `same_domain` vs `cross_domain`

- 추가로 고려할 수 있는 선택
  1. `k=1` 추가
     - very early degradation onset을 더 잘 본다.
  2. `k=6` 또는 `k=12` 같은 중간값
     - curve shape를 더 매끈하게 본다.
  3. token-length matched control
     - 같은 `k` 안에서도 길이 때문인지 turn 구조 때문인지 더 분리 가능
  4. difficulty-matched dummy sampling
     - same/cross뿐 아니라 dummy difficulty를 맞춰 간섭 해석을 더 깨끗하게 할 수 있다.
  5. mixed dummy packs
     - `same_domain` / `cross_domain` 를 섞은 혼합형 pack
     - 현실 대화에는 더 가까우나 해석은 어려워진다.
  6. target-turn-only control
     - target turn만 `/no_think` / prefill / constrained decoding
     - 현재 가장 유망한 follow-up이다.
  7. controlled wrong-answer dummy history
     - gold / self-generated / explicitly wrong dummy answers 를 분리해서 비교

- 지금 시점의 판단
- 가장 먼저 할 것은 `k` grid를 더 늘리는 것이 아니라,
- **target final-answer emission을 안정화** 하는 것이다.
- 그 다음에야 `k=1` 추가나 token-length control이 의미가 있다.
-
- 정리하면:
  - primary: accumulated-history mechanism axes
  - primary(extended): `oracle_history / self_history / wrong_history`
  - secondary: reasoning-mode / emission-control axes

## 2.3 Cross-model context policy (recommended)

- **dummy question manifest는 모든 모델에 공통으로 고정**
  - target마다 어떤 dummy IDs를 붙일지는 shared manifest로 유지한다.
  - 그래야 모델 비교에서 context composition drift가 줄어든다.
- `oracle_history`
  - 모든 모델에 공통 gold answer history를 넣는다.
  - 즉, 같은 target / 같은 `k` / 같은 dummy pack이면 입력 조건이 거의 동일하다.
- `self_history`
  - **평가하는 모델별로 따로 생성**한다.
  - 이유: self_history의 핵심은 “모델 자신의 이전 답변이 후속 target을 얼마나 오염시키는가”이기 때문이다.
- 따라서 권장 해석은:
  - manifest는 shared
  - oracle는 shared
  - self만 model-specific

### Why this is the right default

- manifest까지 모델별로 바꾸면
  - 성능 차이가 model 차이인지
  - dummy sampling 차이인지
  - domain mix 차이인지
  분리가 어려워진다.
- 반대로 self_history까지 완전히 공통으로 고정하면
  - 그건 self contamination이 아니라
  - **external contaminated history robustness** 실험이 된다.

### Optional extra control

- 예산이 남으면 추가 ablation으로
  - **fixed generated history**
  - 즉, 특정 reference model이 만든 history를 모든 모델에 공통 입력
  을 둘 수 있다.
- 하지만 이건 primary protocol이 아니라 **secondary control** 로 두는 것이 좋다.

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

- GPU 5,6 / GPQA / Qwen3 thinking-on / choice constrained only
  - config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_choiceconstrained.yaml`
  - run id: `run-20260311T091942Z-f3e9f0fa`
  - num_items: `8`
  - accuracy: `0.25`
  - format_failure_rate: `0.0`
  - parsed_count / invalid_count: `8 / 0`

- GPU 5,6 / GPQA / Qwen3 thinking-on / `/no_think` + prefill
  - config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_nothink_prefill.yaml`
  - run id: `run-20260311T092221Z-dfa04164`
  - num_items: `8`
  - accuracy: `0.375`
  - format_failure_rate: `0.0`
  - parsed_count / invalid_count: `8 / 0`

- GPU 5,6 / GPQA / Qwen3 thinking-on / choice constrained + `/no_think` + prefill
  - config: `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_choiceconstrained_nothink_prefill.yaml`
  - run id: `run-20260311T092432Z-dac259a0`
  - num_items: `8`
  - accuracy: `0.375`
  - format_failure_rate: `0.0`
  - parsed_count / invalid_count: `8 / 0`

## 4. Immediate experiment checklist

- [x] GPU 5에서 GPQA thinking-on parserfix smoke 1회
- [x] 첫 true GPU567-cycle result를 문서화
- [x] allowed subset `5,6`으로 multi-GPU smoke 1회
- [x] invalid 4건 원인 확인
- [x] GPU 6 또는 7에서 follow-up single-GPU rerun 1회
- [x] AIME fresh numeric rerun 1회
- [x] choice constrained GPQA thinking-on on GPUs `5,6`
- [x] `/no_think` + prefill GPQA thinking-on on GPUs `5,6`
- [x] combined constrained + `/no_think` + prefill GPQA thinking-on on GPUs `5,6`

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
  - pure choice constraint는 형식은 잡지만 all-`A` 쏠림으로 정확도를 깎는다.
  - `/no_think` + prefill은 parserfix baseline 정확도(`0.375`)를 유지하면서 format failure를 `0.0`으로 만들었다.
  - combined config도 같은 정확도를 냈지만, 현재는 **단순한 `/no_think` + prefill**이 active winner다.
  - 다만 이것은 어디까지나 **GPQA thinking-on rescue lane** 에 대한 이야기이고,
  - CRB 전체 연구의 중심은 여전히 `k / mode / history / domain` 축이다.

## 7. Research-backed improvement bets

- Qwen 공식 문서 기준
  - thinking mode 권장 샘플링은 `temperature=0.6`, `top_p=0.95`, `top_k=20`
  - `/think`, `/no_think` soft switch 또는 assistant prefill `<think>\n\n</think>\n\n` 로 turn-level 제어 가능
- vLLM 공식 문서 기준
  - structured outputs `choice` / `regex` 제약을 offline/online 모두 지원
- 따라서 다음 우선 실험 제안
  1. `k={0,2,4,8}` sweep으로 dummy-turn accumulation curve를 채우기
  2. `self_history vs oracle_history`, `same_domain vs cross_domain`, `multi_turn vs flattened` 차이를 먼저 확보하기
  3. thinking on/off는 위 protocol rows 위에서 secondary comparison으로 읽기
  4. GPQA thinking-on rescue lane은 `/no_think` + prefill을 유지하되, headline objective로 두지 않기

## 8. Implemented experiment configs and fresh outcomes

- [x] choice constrained GPQA thinking-on config 추가
  - `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_choiceconstrained.yaml`
  - result: `run-20260311T091942Z-f3e9f0fa` / accuracy `0.25` / format failure `0.0`
- [x] target `/no_think` + response prefill config 추가
  - `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_nothink_prefill.yaml`
  - result: `run-20260311T092221Z-dfa04164` / accuracy `0.375` / format failure `0.0`
- [x] choice constrained + `/no_think` + prefill 결합 config 추가
  - `Legacy/configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on_choiceconstrained_nothink_prefill.yaml`
  - result: `run-20260311T092432Z-dac259a0` / accuracy `0.375` / format failure `0.0`
- [x] mock config / tests로 generation-control plumbing 검증
  - `Legacy/configs/mock_mmlu_multiturn_oracle_constrained_nothink.yaml`

## 9. Deferred next-step checklist

- [x] GPU available when ready
- [x] Run choice constrained GPQA thinking-on on allowed GPU set
- [x] Run `/no_think` + prefill GPQA thinking-on on allowed GPU set
- [x] Run combined constrained + `/no_think` + prefill GPQA thinking-on on allowed GPU set
- [x] Compare against current parserfix baseline:
  - `run-20260311T060823Z-1947f5cf`
- [x] Compare against strictfinal follow-up:
  - `run-20260311T063838Z-7956de92`
- [x] Record whether invalids shift from parse_failure to wrong-answer
- [x] Record whether accuracy recovers without raising format failure
- [x] Append results to `docs/RESULTS_LOG.md`
- [x] Summarize winner in `docs/ANALYSIS.md`
- [ ] Replicate `/no_think` + prefill once more on GPUs `5,6`
- [ ] Decide whether combined config is worth keeping beyond fallback use
- [ ] Port the winning control to GSM8K or MMLU
