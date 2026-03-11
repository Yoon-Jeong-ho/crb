# Training Verifiers to Solve Math Word Problems (GSM8K)

- Citation: Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, John Schulman. 2021.
- Venue: arXiv / OpenAI 2021
- Source: https://arxiv.org/abs/2110.14168

## 핵심 내용
- GSM8K를 소개하고, LLM이 multi-step math reasoning에서 여전히 약함을 보인다.
- verifier-based reranking이 성능을 크게 올릴 수 있다고 주장한다.

## 왜 CRB와 관련 있는가
- CRB의 핵심 수학 benchmark 축이다.
- 숫자형 short answer라서 **format robustness** 와 **reasoning robustness** 를 분리해 보기 좋다.

## CRB와의 차이
- GSM8K 원 논문은 주로 math reasoning 자체와 verifier training을 본다.
- CRB는 GSM8K를 **history accumulation interference** 측정 도구로 사용한다.
- 즉, 수학 reasoning 능력 자체보다, 앞선 turn이 마지막 math answer를 얼마나 흔드는지 본다.

## CRB 논문에서 어떻게 쓰면 좋은가
- GSM8K는 “short answer numeric benchmark” 축으로 소개한다.
- GPQA보다 parser가 단순해서 self/oracle history contamination을 수학 영역에서 더 깨끗하게 볼 수 있다고 연결하면 좋다.

## 우리에게 주는 시사점
- GSM8K는 final-answer emission 제어 실험에 특히 좋다.
- thinking on/off 비교가 GPQA보다 덜 noisy할 가능성이 있다.
