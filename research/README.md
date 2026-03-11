# CRB Research Notes

이 폴더는 CRB와 직접적으로 관련된 논문들을 빠르게 재사용할 수 있도록 정리한 리서치 메모 모음이다.

## 폴더 구성
- `papers/` — 논문별 1개 md 파일
- 이 `README.md` — 전체 지형도, CRB와의 차이, 강조 포인트, 추가 분석 제안

## 가장 중요한 논문 묶음

### 1) 우리가 사용하는 benchmark 자체를 정당화하는 논문
- MMLU — `papers/mmlu.md`
- GSM8K — `papers/gsm8k.md`
- GPQA — `papers/gpqa.md`

### 2) 긴 입력/긴 컨텍스트가 성능을 해칠 수 있음을 보여주는 논문
- Lost in the Middle — `papers/lost_in_the_middle.md`
- LongBench — `papers/longbench.md`
- Same Task, More Tokens — `papers/same_task_more_tokens.md`
- RULER — `papers/ruler.md`
- BABILong — `papers/babilong.md`
- Summary of a Haystack — `papers/summary_of_a_haystack.md`

### 3) 멀티턴 대화 평가와 비교할 논문
- MT-Bench / LLM-as-a-Judge — `papers/mt_bench_llm_judge.md`

## 이 논문들과 CRB의 핵심 차이

### CRB는 단순 long-context benchmark가 아니다
기존 long-context 논문 상당수는 다음 중 하나에 집중한다.
- 긴 문서에서 정보 retrieval
- long-context QA / summarization
- synthetic reasoning task
- position bias / token length degradation

CRB는 다르다.
- **표준 benchmark 문제(MMLU/GSM8K/GPQA/AIME)를 그대로 유지**한다.
- 단지 앞에 **dummy turn**을 누적해서 마지막 target question 성능이 얼마나 흔들리는지 본다.
- 즉, "새 long-context task"가 아니라 **기존 benchmark를 multi-turn accumulated-history setting으로 재평가**한다.

### CRB는 마지막 target만 채점한다
이 점이 중요하다.
- 기존 multi-turn benchmark는 대화 전체 품질/선호도를 보는 경우가 많다.
- CRB는 **앞의 turn은 방해 요인(dummy history)** 이고, **마지막 target correctness만 score** 한다.
- 따라서 "대화를 잘하느냐"보다 **누적 히스토리 간섭에 견디느냐**를 본다.

### CRB는 간섭 메커니즘을 분해한다
CRB는 단순 정확도 하락을 보는 것이 아니라, 다음 요인을 분해할 수 있다.
- `multi_turn` vs `single_turn_flattened`
- `self_history` vs `oracle_history`
- `same_domain` vs `cross_domain`
- `k=0,2,4,8`
- same-family `thinking on/off`

이 조합은 기존 long-context benchmark보다 **원인 해석이 훨씬 쉽다**.

## CRB가 논문에서 강조해야 할 것

### 1) “length”가 아니라 “accumulated interference”
논문 메시지를 단순히 "길어지면 성능이 떨어진다" 로 쓰면 약하다.
CRB가 강조해야 하는 것은:
- 단순 token length 증가가 아니라
- **turn-structured accumulated history** 와
- **이전 답변(self history) 오염** 과
- **domain-aligned distractor** 가
최종 target 성능을 어떻게 무너뜨리는가이다.

### 2) 기존 benchmark를 재활용하면서 새로운 failure mode를 드러낸다
CRB는 새로운 task를 만들기보다,
- 이미 널리 쓰이는 benchmark를
- 새 evaluation protocol로 다시 본다.

이건 논문적으로 장점이다.
- benchmark 신뢰성은 기존 논문이 이미 받쳐준다.
- novelty는 dataset 자체가 아니라 **evaluation protocol** 과 **mechanism isolation** 에 있다.

### 3) “reasoning quality”와 “format robustness”를 분리해 보여라
현재 실험에서도 보이듯이,
- accuracy 하락
- parse failure / final-answer emission failure
이 함께 발생한다.

CRB는 반드시 다음을 분리해서 보여야 한다.
- 정답을 냈는데 format이 틀린 경우
- format은 맞는데 오답인 경우
- self_history 때문에 후속 질문 reasoning이 흐트러지는 경우

### 4) same-domain 간섭은 좋은 메시지 후보
same-domain dummy가 cross-domain보다 더 강한 간섭을 주면,
이건 "단순한 잡음"이 아니라 **semantic interference** 라는 메시지로 연결된다.

### 5) thinking on/off는 좋은 실험 축이지만 주 메시지는 아니다
thinking on/off는 분명 흥미롭지만,
논문의 중심축은 다음이 더 강하다.
- accumulated history interference
- self vs oracle contamination
- same vs cross domain interference
- turn structure vs flattened control

thinking on/off는 **secondary but valuable axis** 로 두는 편이 안전하다.

## 논문 작성 방향 제안

### 추천 서사
1. 표준 single-turn benchmark는 현실의 누적 대화 상태를 반영하지 못한다.
2. long-context 결과만으로는 왜 성능이 무너지는지 분해하기 어렵다.
3. 우리는 benchmark item 자체는 유지하고 evaluation protocol만 바꾼다.
4. 이를 통해 accumulated history가 final target에 미치는 영향을 정량화한다.
5. 그리고 그 영향을 self/oracle, same/cross, multi/flattened, k, thinking on/off로 분해한다.

### Related Work 섹션 구조
1. Standard benchmark papers
   - MMLU / GSM8K / GPQA
2. Long-context robustness / position bias
   - Lost in the Middle / LongBench / Same Task, More Tokens / RULER / BABILong / Summary of a Haystack
3. Multi-turn chat evaluation
   - MT-Bench
4. Our difference
   - target-only scoring under accumulated conversational history

### Claim wording
좋은 표현:
- “conversation-accumulated interference”
- “target-only evaluation under multi-turn history”
- “history contamination”
- “turn-structured interference beyond pure length effects”

피하는 표현:
- “just another long-context benchmark”
- “general chat benchmark”
- “reasoning benchmark” 단독 표현

## 추가적으로 꼭 해볼 분석

### 우선순위 높음
1. **item-level paired delta**
   - 같은 target item이 `k` 증가에 따라 어떻게 변하는지
2. **accuracy vs format failure 분해**
   - degradation의 몇 %가 parse failure인지
3. **self vs oracle gap**
   - contamination의 직접 근거
4. **same vs cross gap**
   - semantic interference의 직접 근거
5. **multi_turn vs flattened**
   - turn structure effect의 직접 근거

### 우선순위 중간
6. **token-length matched control**
   - 길이는 비슷한데 turn structure만 다른 경우
7. **dataset별 민감도 차이**
   - GPQA / GSM8K / AIME / MMLU-family
8. **thinking on/off를 accuracy와 format으로 분해**
   - reasoning quality vs answer emission robustness
9. **bootstrap / confidence interval**
   - 작은 pilot/mini 결과의 불안정성 완화
10. **seed / manifest robustness**
   - dummy sampling 특정성 점검

### 있으면 좋은 분석
11. target turn 위치를 고정한 상태에서 total token 수 통제
12. self_history raw vs canonicalized history 비교
13. invalid output taxonomy
   - no final answer
   - multiple answers
   - reasoning only
   - malformed numeric

## 지금까지 실험 기준으로 본 실전 해석
- GPQA thinking-off는 baseline으로 충분히 안정적이다.
- GPQA thinking-on은 parserfix 후에도 개선은 있지만 아직 final-answer emission 문제가 남아 있다.
- strict-final prompting은 parseability를 올릴 수 있지만 정확도를 희생할 수 있다.
- 따라서 next step은 parser regex 추가보다 **answer emission control** 쪽이다.

## 추천 다음 액션
1. GPQA target turn에 MCQ constrained decoding 실험
2. target turn만 `/no_think` 또는 prefill 적용 실험
3. GSM8K 또는 MMLU continuation run으로 일반성 확인
