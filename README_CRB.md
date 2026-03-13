# CRB: Conversation-Accumulated Robustness Benchmark

CRB는 기존 single-turn benchmark를 **multi-turn accumulated history** 환경으로 변환해, 모델이 앞선 대화 히스토리와 더미 문제들 때문에 마지막 실제 평가 문제에서 얼마나 성능이 흔들리는지 측정하기 위한 실험 프레임워크입니다.

핵심 질문은 다음과 같습니다.

- 앞에 들어가는 **k개의 dummy turn** 이 마지막 target 정확도를 얼마나 떨어뜨리는가?
- 이 간섭은 dummy의 **정답/오답/모델 자신의 이전 답변(self history)** 에 따라 어떻게 달라지는가?
- 같은 domain dummy와 다른 domain dummy는 어떤 식으로 다른 간섭을 만드는가?
- 멀티턴 히스토리가 누적되면 성능은 얼마나 감소하는가?
- 이 감소는 단순 context length 때문인가, 아니면 **turn-structured history** 자체 때문인가?
- 앞선 더미 문제에 대한 모델의 실제 응답이 후속 문제까지 오염시키는가?
- 같은 domain의 더미가 더 강한 간섭을 만드는가?
- 같은 모델 패밀리 안에서 **thinking on/off**는 이 간섭을 악화/완화하는 **부차적 축**으로 어떻게 작동하는가?

---

## 1. 실험 개요

각 target question에 대해:

1. 먼저 채점하지 않는 **dummy question k개**를 앞선 턴들에 넣습니다.
2. 모델이 각 dummy에 답합니다.
3. 마지막 턴에만 실제 **target question**을 넣습니다.
4. **마지막 target의 정답 여부만 점수화**합니다.

이 과정을 통해 single-turn benchmark에서는 보이지 않던 **conversation-accumulated interference**를 측정합니다.

---

## 2. 핵심 실험 축

CRB의 핵심은 **모델 자체 비교**보다 먼저, 아래 **protocol axis** 를 통해 accumulated interference를 분해하는 것이다.
`thinking on/off`는 그 위에 얹는 **secondary analysis axis** 이다.

### Evaluation mode
- `multi_turn`: 실제 user/assistant turn 구조 유지
- `single_turn_flattened`: 이전 QA를 하나의 긴 프롬프트로 평탄화

### History mode
- `self_history`: dummy에 대한 모델의 실제 답을 history에 사용
- `oracle_history`: dummy에 대한 gold answer만 history에 사용

즉, 앞의 k개 dummy는 단순 distractor가 아니라:
- **gold canonical answer** 가 들어갈 수도 있고 (`oracle_history`)
- **모델 자신의 실제 이전 답변 / reasoning leakage** 가 들어갈 수도 있다 (`self_history`)

### Dummy type
- `same_domain`: target과 같은 subject/domain에서 dummy 추출
- `cross_domain`: target과 다른 subject/domain에서 dummy 추출

### k values
- 메인 비교: `k ∈ {0, 2, 4, 8}`
- smoke/pilot: 기본적으로 `k=2`

---

## 3. 지원 데이터셋

### MMLU-family
- 일반 지식형 객관식 anchor benchmark
- 현재 구현은 MMLU-style adapter 중심
- clean benchmark 교체/병행은 추후 실험 설계에 따라 확장 가능

### GSM8K
- 수학형 short/numeric benchmark
- history accumulation이 arithmetic reasoning에 주는 영향 측정

### GPQA
- 고난도 과학 객관식 benchmark
- science reasoning에서 multi-turn interference 측정

### AIME
- 정수형 정답 중심의 수학 benchmark
- numeric parser / evaluator 검증 및 tougher math setting 확장

---

## 4. 지원 모델

### 현재 핵심 모델
- `Qwen3-1.7B` thinking off
- `Qwen3-1.7B` thinking on

### 설계상 확장 가능 모델
- 더 큰 Qwen3 계열
- DeepSeek distill reasoning 계열
- Gemma instruct 계열

현재 본문 핵심 비교는
- **k dummy turns**
- **multi_turn vs flattened**
- **self_history vs oracle_history**
- **same_domain vs cross_domain**
를 먼저 보는 것이고,
`Qwen3 thinking on/off`는 이 위에 얹는 **secondary but valuable axis** 입니다.

---

## 5. 엔진 및 환경

### 엔진
- `vLLM`

### conda env
- `/data_x/aa007878/projects/crb/.conda/envs/crb`

### GPU 사용 규칙
- 기본: `CUDA_VISIBLE_DEVICES=6,7`
- 단일 GPU 디버깅: `CUDA_VISIBLE_DEVICES=6`
- 다른 GPU는 사용하지 않는 것을 기본 원칙으로 함

### 환경 원칙
- 프로젝트 내부에 새로운 `.venv`, 별도 `.conda` sandbox 추가 생성 금지
- 설치 변경 시 `environment.yml`, `requirements.txt`를 함께 갱신

---

## 6. 디렉토리 구조

예상 구조는 아래와 같습니다.

```text
.
├── configs/
│   ├── templates/
│   ├── sweeps/
│   └── *.yaml
├── docs/
│   ├── EXECUTION_STATUS.md
│   ├── RESULTS_LOG.md
│   ├── ANALYSIS.md
│   ├── TODO_NEXT.md
│   └── EXPERIMENT_PLAN.md
├── results/
│   ├── runs/
│   ├── summary/
│   └── analysis/
├── scripts/
├── src/crb/
├── tests/
├── environment.yml
├── requirements.txt
└── README.md
```

---

## 7. 실행 흐름

### 7.1 기본 원칙
실험은 항상 아래 순서로 진행합니다.

1. 상태 점검
2. smoke test
3. mini run
4. main sweep
5. 결과 검증
6. 분석 문서화
7. git commit / push

### 7.2 smoke test 예시

```bash
CUDA_VISIBLE_DEVICES=6 \
python -m src.crb.run_eval --config configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off.yaml
```

### 7.3 thinking on 예시

```bash
CUDA_VISIBLE_DEVICES=6 \
python -m src.crb.run_eval --config configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on.yaml
```

### 7.4 batch / sweep 예시

```bash
bash scripts/materialize_qwen3_core_sweep.sh
bash scripts/run_qwen3_core_sweep.sh
```

실제 entrypoint 이름은 저장소 구현에 맞춰 조정하면 됩니다.

---

## 8. 출력 형식

### Run-level JSON
각 실험(run)마다 상세 결과 JSON을 하나 생성합니다.

예시 필드:
- `run_id`
- `timestamp`
- `git_commit`
- `model_name`
- `model_family`
- `thinking_mode`
- `dataset`
- `evaluation_mode`
- `history_mode`
- `dummy_type`
- `k`
- `metrics`
- `per_item_results`

### Cumulative CSV
하나의 scoreboard CSV에 전체 run 요약을 누적합니다.

예시 컬럼:
- `timestamp`
- `run_id`
- `git_commit`
- `model_name`
- `model_family`
- `thinking_mode`
- `dataset`
- `evaluation_mode`
- `history_mode`
- `dummy_type`
- `k`
- `accuracy`
- `format_failure_rate`
- `result_json_path`

---

## 9. 채점 원칙

### MCQ
- 최종 응답 형식 예시: `Answer: B`
- option letter exact match
- ambiguous output은 invalid 처리

### Numeric
- 최종 응답 형식 예시: `Answer: 42`
- normalization 후 exact match
- parse 실패는 invalid 처리

### 공통
- reprompt는 하지 않음
- 기본 history에는 **canonicalized answer만 저장**

---

## 10. 문서 운영 규칙

실험은 코드만이 아니라 문서까지 함께 운영합니다.

### `docs/EXECUTION_STATUS.md`
- 현재 환경 상태
- 준비된 config
- GPU 상태
- pending runs
- blocker

### `docs/RESULTS_LOG.md`
- 날짜별 실행 기록
- 성공/실패
- JSON 경로
- scoreboard 반영 여부

### `docs/ANALYSIS.md`
- 현재까지의 핵심 관찰
- Qwen3 thinking on/off 비교
- dataset별 차이
- preliminary findings

### `docs/TODO_NEXT.md`
- 다음 실행 우선순위
- 미검증 config
- 남은 리스크

### `docs/EXPERIMENT_PLAN.md`
- 파일럿 → 본 실험 전체 계획
- sweep 진행도

---

## 11. 권장 실험 순서

### 파일럿
1. GPQA + multi_turn + oracle + same_domain + k=2
2. GSM8K + flattened + self + cross_domain + k=2
3. AIME + numeric evaluator 확인
4. 그 다음에 같은 조건 위에 thinking on/off를 얹어 secondary comparison 수행

### 미니 런
- smoke 성공 설정에 대해 `num_samples` 증가
- parser failure, timeout, malformed output, scoreboard append 검증

### 본 실험
최소 비교 축:
- dataset: MMLU-family, GSM8K, GPQA, AIME
- mode: multi_turn, single_turn_flattened
- history: self_history, oracle_history
- dummy: same_domain, cross_domain
- k: 0,2,4,8
- model/reasoning mode: Qwen3 thinking off/on (**secondary axis**)

---

## 12. 분석 시 확인할 항목

- accuracy vs k
- multi_turn vs flattened 차이
- self_history vs oracle_history 차이
- same_domain vs cross_domain 차이
- thinking on/off 차이 (secondary)
- dataset별 robustness 패턴
- format failure rate

---

## 13. 현재 상태 표기 원칙

README와 docs에서는 아래를 반드시 구분합니다.

- **구현 완료**: 코드와 config가 존재함
- **실행 검증 완료**: 실제 JSON/CSV 결과가 생성됨
- **본 실험 완료**: 논문용 주요 sweep이 끝남

즉, “지원한다”와 “실제로 검증했다”를 섞어 쓰지 않습니다.

---

## 14. Git 운영 원칙

- 의미 있는 단계마다 commit
- 실험 결과가 생기면 commit 후보
- docs 갱신도 commit
- README 갱신도 commit
- push를 반복적으로 수행
- commit message는 실행/분석/문서 변경이 드러나게 구체적으로 작성

예시:
- `run gpqa multiturn oracle thinking-off smoke test`
- `validate aime numeric parsing end-to-end`
- `update analysis docs after qwen3 thinking comparison`

---

## 15. 현재 권장 다음 단계

1. GPQA thinking off 실제 smoke run
2. Qwen3 thinking on 실제 run 1개 확보
3. AIME numeric run 검증
4. scoreboard에 thinking_mode 포함 신규 row 생성 확인
5. docs/RESULTS_LOG.md, docs/ANALYSIS.md 갱신
6. 이후 `k=0,2,4,8` 확장 sweep 진행

---

## 16. 참고 문서

- `CRB_EXPERIMENT_SETUP.md`: 실험 운영용 상세 셋업 문서
- `docs/EXECUTION_STATUS.md`: 현재 진행 상태
- `docs/RESULTS_LOG.md`: 실행 이력
- `docs/ANALYSIS.md`: 결과 해석
- `docs/TODO_NEXT.md`: 다음 액션

---

## 17. 요약

CRB는 기존 single-turn benchmark를 대화 누적 환경으로 변환해,
모델이 **앞선 더미 문제와 대화 히스토리 때문에 마지막 문제에서 얼마나 성능이 흔들리는지**를 측정하는 프레임워크입니다.

핵심은 단순 context length가 아니라,
- turn-structured history
- self-error accumulation
- domain-specific interference
- reasoning mode 차이
를 함께 보는 데 있습니다.
