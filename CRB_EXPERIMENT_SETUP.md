# CRB Experiment Setup

## 1. 목적

이 문서는 CRB(Conversation-Accumulated Robustness Benchmark) 실험을 **파일럿 → 디버깅 → 본 실험 → 분석 → 문서화** 순서로 안정적으로 진행하기 위한 운영용 셋업 문서다.  
핵심 목표는 기존 single-turn benchmark를 multi-turn accumulated history 환경으로 변환했을 때, 모델의 최종 성능이 어떻게 흔들리는지 정량화하는 것이다.

이 문서는 다음을 다룬다.
- 사용할 데이터셋
- 사용할 모델군
- 실험 축과 설정값
- 파일럿 실험 절차
- 본 실험 절차
- 결과 저장 규칙
- 분석 항목
- 체크리스트
- 리스크 및 주의사항

---

## 2. 연구 질문

### RQ1. 
멀티턴 히스토리가 누적되면, 기존 single-turn benchmark 성능은 얼마나 감소하는가?

### RQ2.
이 성능 저하는 단순한 context length 증가 때문인가, 아니면 **turn-structured history** 자체 때문인가?

### RQ3.
앞선 더미 문제에 대한 모델의 실제 응답(self history)이 후속 문제까지 오염시키는가?

### RQ4.
같은 도메인의 더미가 다른 도메인의 더미보다 더 강한 간섭을 일으키는가?

### RQ5.
같은 모델 패밀리 안에서 **Qwen3 thinking on/off**는 누적 히스토리 간섭에 대해 다른 강건성을 보이는가?

---

## 3. 핵심 실험 개념

### 3.1 Target question 평가 방식
각 평가 샘플에 대해:
1. 먼저 채점하지 않는 **dummy question k개**를 앞선 턴들에 넣는다.
2. 모델이 각 dummy에 답한다.
3. 마지막 턴에만 실제 **target question**을 넣는다.
4. **마지막 target의 정답 여부만 점수화**한다.

### 3.2 비교할 evaluation mode
- `multi_turn`
  - 실제 user/assistant turn 구조를 유지한다.
- `single_turn_flattened`
  - 이전 QA를 하나의 긴 프롬프트로 평탄화하여 마지막 문제만 답하게 한다.

### 3.3 비교할 history mode
- `self_history`
  - 더미 문제에 대해 모델이 실제로 생성한 정규화된 답을 history에 넣는다.
- `oracle_history`
  - 더미 문제에 대한 gold answer만 history에 넣는다.

### 3.4 비교할 dummy type
- `same_domain`
  - target과 같은 subject/domain에서 dummy를 뽑는다.
- `cross_domain`
  - target과 다른 subject/domain에서 dummy를 뽑는다.

### 3.5 k 값
- 메인 비교: `k ∈ {0, 2, 4, 8}`
- 파일럿/스모크 테스트: 우선 `k=2`
- 필요 시 확장: `k=16`은 appendix 또는 후속 실험

---

## 4. 데이터셋 구성

본 실험에서는 **지식형 / 수학형 / 과학형**을 모두 포함한다.

### 4.1 MMLU-family
- 목적: 일반 지식형 객관식 성능 측정
- 역할: benchmark의 기본 anchor
- 주의: 현재 구현상 `cais/mmlu` 계열 adapter를 사용 중이며, 본문용 실험에서는 clean benchmark 사용 여부를 재검토한다.

### 4.2 GSM8K
- 목적: 정답 추출이 쉬운 수학형 benchmark
- 답 형식: numeric / short answer
- 역할: 수학 reasoning에서 history accumulation 효과 측정

### 4.3 GPQA
- 목적: 고난도 과학 객관식 benchmark
- 답 형식: multiple-choice
- 역할: 고난도 science reasoning에서 multi-turn interference 측정

### 4.4 AIME
- 목적: 정수형 정답 중심의 수학 benchmark
- 답 형식: numeric exact match
- 역할: 더 엄격한 수학형 평가 축 추가
- 주의: domain이 거의 math 단일이므로 `cross_domain` 정의 시 cross-dataset dummy 사용 여부를 명시해야 함

### 4.5 데이터셋 우선순위
#### 파일럿 우선순위
1. GPQA
2. GSM8K
3. AIME
4. MMLU-family

#### 본 실험 우선순위
1. GPQA
2. GSM8K
3. MMLU-family
4. AIME

---

## 5. 모델 구성

### 5.1 핵심 비교 모델
본 실험의 핵심은 **같은 패밀리 내에서 thinking on/off 비교**다.

#### Qwen3 1.7B
- `thinking_mode = off`
- `thinking_mode = on`
- 목적: 동일 backbone에서 reasoning mode 차이를 비교
- 이유: 논문 메시지의 핵심 축 중 하나

### 5.2 후속 확장 모델
본 실험이 안정화된 뒤 추가 검토
- Qwen3 더 큰 모델
- DeepSeek distill reasoning 계열
- Gemma instruct 계열

### 5.3 모델 우선순위
#### 파일럿
- Qwen3-1.7B thinking off
- Qwen3-1.7B thinking on

#### 본 실험
- 위 두 조건을 최소 기준으로 유지
- 여력이 있으면 larger Qwen3 또는 타 family 추가

---

## 6. 엔진 및 환경

### 6.1 엔진
- `vLLM` 고정

### 6.2 환경
- conda env: `/data_x/aa007878/projects/crb/.conda/envs/crb`
- Python / torch / transformers / vllm 버전은 현재 저장소 기준을 따른다.

### 6.3 GPU 사용 규칙
- 기본: `CUDA_VISIBLE_DEVICES=6,7`
- 단일 GPU 디버깅: `CUDA_VISIBLE_DEVICES=6`
- 다른 GPU는 사용하지 않음

### 6.4 운영 원칙
- 새 env 만들지 않음
- 프로젝트 내부 추가 sandbox 만들지 않음
- 설치 변경 시 `environment.yml`, `requirements.txt`, `README`에 반영

---

## 7. 프롬프트 및 채점 원칙

### 7.1 공통 원칙
- 모델의 최종 응답은 **정규화된 final answer**가 반드시 포함되어야 한다.
- history에는 기본적으로 **canonicalized answer만 저장**한다.
- reasoning text를 그대로 history에 누적하는 것은 기본값으로 사용하지 않는다.

### 7.2 객관식
예시 형식:
- `Answer: B`

### 7.3 수학형
예시 형식:
- `Answer: 42`

### 7.4 채점 방식
- MCQ: option letter exact match
- Numeric: normalization 후 exact match
- parse 실패 또는 ambiguous output은 invalid 처리
- reprompt는 하지 않음

---

## 8. 파일럿 실험 계획

파일럿 목표는 **코드가 돈다**가 아니라, 아래를 실제로 검증하는 것이다.
- dataset adapter가 실제로 로드됨
- parser / evaluator가 실제 데이터에서 동작함
- thinking on/off가 실제 config와 결과에 반영됨
- JSON과 scoreboard가 올바르게 저장됨
- smoke → mini run으로 확장 가능한 상태인지 확인됨

### 8.1 파일럿 단계 1: smoke test
작은 `num_samples`로 end-to-end 동작 확인

#### Pilot-1
- dataset: GPQA
- model: Qwen3-1.7B thinking off
- mode: multi_turn
- history: oracle_history
- dummy: same_domain
- k=2

#### Pilot-2
- dataset: GPQA 또는 GSM8K
- model: Qwen3-1.7B thinking on
- mode: flattened 또는 multi_turn
- history: self_history 또는 oracle_history
- k=2

#### Pilot-3
- dataset: AIME
- model: Qwen3-1.7B thinking off
- mode: multi_turn
- history: oracle_history
- dummy: same_domain
- k=2
- 목적: numeric parsing/evaluation 검증

### 8.2 파일럿 단계 2: mini run
- smoke test가 성공한 설정을 대상으로 `num_samples`를 늘린다.
- 여기서 봐야 할 것:
  - parser failure rate
  - timeout
  - malformed output
  - dummy sampling 이상 여부
  - result JSON의 필드 누락 여부
  - scoreboard append 정상 여부

### 8.3 파일럿 종료 기준
아래를 모두 만족하면 본 실험으로 넘어간다.
- GPQA 1개 이상 성공
- Qwen3 thinking on/off 각각 최소 1개 run 성공
- AIME numeric run 성공
- run JSON 생성 확인
- scoreboard 신규 row 확인
- docs/ 결과 로그 갱신 완료

---

## 9. 본 실험 계획

### 9.1 본 실험 핵심 축
- dataset: `mmlu-family`, `gsm8k`, `gpqa`, `aime`
- model: `qwen3 thinking off`, `qwen3 thinking on`
- evaluation_mode: `multi_turn`, `single_turn_flattened`
- history_mode: `self_history`, `oracle_history`
- dummy_type: `same_domain`, `cross_domain`
- k: `0, 2, 4, 8`

### 9.2 실행 순서
#### Phase A. 논문 메시지 확인용 핵심 결과
우선 가장 빨리 메시지를 볼 수 있는 비교부터 진행
1. GPQA: off vs on
2. GSM8K: off vs on
3. GPQA: multi_turn vs flattened
4. GPQA: self vs oracle
5. GPQA: same vs cross

#### Phase B. 핵심 축 확장
- k=0,2,4,8 sweep
- dataset 확장: MMLU-family, AIME

#### Phase C. 논문 표/그림용 결과 확보
- 모든 주요 dataset에 대해 최소 off/on pair 확보
- same/cross, self/oracle, multi/flattened 비교 표 작성 가능 수준까지 확장

### 9.3 본 실험 최소 성공 조건
아래 비교는 최소한 확보해야 한다.
1. Qwen3 thinking off vs on (같은 dataset, 같은 k, 같은 mode)
2. multi_turn vs flattened
3. self_history vs oracle_history
4. same_domain vs cross_domain
5. k 증가에 따른 accuracy degradation

---

## 10. 산출물 규칙

### 10.1 Run JSON
각 run마다 상세 JSON 생성
필수 필드:
- run_id
- timestamp
- git_commit
- model_name
- model_family
- thinking_mode
- dataset
- evaluation_mode
- history_mode
- dummy_type
- k
- seed
- num_items
- metrics
- config
- per_item_results

### 10.2 Scoreboard CSV
하나의 누적 CSV 유지
필수 컬럼:
- timestamp
- run_id
- git_commit
- model_name
- model_family
- thinking_mode
- dataset
- split
- evaluation_mode
- history_mode
- dummy_type
- k
- seed
- num_items
- accuracy
- format_failure_rate
- result_json_path

### 10.3 분석 문서
지속적으로 업데이트할 md 파일
- `docs/EXECUTION_STATUS.md`
- `docs/RESULTS_LOG.md`
- `docs/ANALYSIS.md`
- `docs/TODO_NEXT.md`
- `docs/EXPERIMENT_PLAN.md`

---

## 11. 분석 계획

### 11.1 필수 분석 항목
1. Accuracy vs k
2. multi_turn vs single_turn_flattened
3. self_history vs oracle_history
4. same_domain vs cross_domain
5. Qwen3 thinking off vs on
6. dataset별 degradation 차이
7. format failure rate

### 11.2 논문용 핵심 메시지 후보
- single-turn에서 높은 점수를 받는 모델도 accumulated history 하에서는 성능이 무너질 수 있다.
- 이 성능 저하는 단순 length 증가보다 turn structure와 history contamination의 영향을 받는다.
- self history는 oracle history보다 더 큰 성능 저하를 유발할 수 있다.
- same-domain dummy는 cross-domain dummy보다 강한 간섭을 일으킬 수 있다.
- thinking on/off는 accumulated interference에 대해 서로 다른 강건성을 보일 수 있다.

### 11.3 후속 확장 분석
- target당 multiple dummy pack 평균
- raw history vs canonicalized history ablation
- AIME의 cross-dataset dummy 설계 영향
- larger Qwen3 또는 타 모델 family 확장

---

## 12. 리스크 및 주의사항

### 12.1 GPU contention
- GPU 6,7이 바쁘면 full run보다 smoke/mini run 또는 문서화/분석 작업 우선

### 12.2 Dataset/domain 정의
- GPQA, MMLU-family는 domain 분리가 비교적 명확
- AIME는 domain이 거의 math 단일이라 cross_domain 정의가 약함
- AIME에서는 cross-dataset dummy 전략을 별도 명시해야 함

### 12.3 README와 실제 실행 상태 구분
- 코드 반영 완료
- config 준비 완료
- 실제 실행 검증 완료
를 항상 구분해서 문서화

### 12.4 라이선스/메타데이터 정합성
- 저장소 LICENSE, pyproject license, README 기술 내용이 서로 일치하는지 점검

---

## 13. 작업 순서 체크리스트

### 13.1 사전 점검
- [ ] git status clean 확인
- [ ] conda env import check
- [ ] GPU 6,7 상태 확인
- [ ] scoreboard 현황 확인
- [ ] docs 상태 확인
- [ ] configs 존재 여부 확인

### 13.2 파일럿
- [ ] GPQA thinking off smoke run
- [ ] GPQA/GSM8K thinking on smoke run
- [ ] AIME numeric smoke run
- [ ] JSON 생성 확인
- [ ] scoreboard row 생성 확인
- [ ] parser / evaluator 이상 여부 점검

### 13.3 미니 런
- [ ] GPQA mini run
- [ ] GSM8K mini run
- [ ] AIME mini run
- [ ] thinking on/off 결과 비교 가능 여부 확인

### 13.4 본 실험 준비
- [ ] k sweep config 확인
- [ ] same/cross 설정 확인
- [ ] self/oracle 설정 확인
- [ ] flattened/multi_turn 설정 확인
- [ ] analysis 스크립트 준비

### 13.5 본 실험
- [ ] GPQA off/on pair
- [ ] GSM8K off/on pair
- [ ] MMLU-family 핵심 비교
- [ ] AIME numeric 본 run
- [ ] k=0,2,4,8 sweep 일부 완료

### 13.6 분석 및 문서화
- [ ] RESULTS_LOG 업데이트
- [ ] ANALYSIS 업데이트
- [ ] TODO_NEXT 업데이트
- [ ] README 업데이트
- [ ] preliminary table/figure용 summary 생성

### 13.7 git 반영
- [ ] 의미 있는 단위 commit
- [ ] push 완료
- [ ] 다음 실행 우선순위 기록

---

## 14. 이번 주 우선 실행 권장안

### Priority 1
- GPQA + Qwen3 thinking off + multi_turn + oracle_history + same_domain + k=2

### Priority 2
- GPQA 또는 GSM8K + Qwen3 thinking on + k=2

### Priority 3
- AIME + numeric evaluator 검증

### Priority 4
- GPQA 기준 off/on pair 확보

### Priority 5
- GPQA 기준 k=0,2,4,8 확장

---

## 15. 완료 기준

다음이 충족되면 “실험 셋업 완료”로 본다.

- GPQA / GSM8K / AIME가 실제로 end-to-end 실행됨
- Qwen3 thinking on/off 둘 다 실제 run 성공
- JSON / scoreboard / docs가 일관되게 갱신됨
- 파일럿에서 본 실험으로 확장 가능한 config와 workflow가 정리됨
- 분석 md 문서가 지속적으로 축적됨
- README가 현재 상태를 정확히 반영함

