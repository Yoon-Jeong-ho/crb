# BABILong: Testing the Limits of LLMs with Long Context Reasoning-in-a-Haystack

- Citation: Yuri Kuratov, Aydar Bulatov, Petr Anokhin, Ivan Rodkin, Dmitry Igorevich Sorokin, Artyom Sorokin, Mikhail Burtsev. 2024.
- Venue: NeurIPS 2024 Datasets and Benchmarks
- Source: https://openreview.net/forum?id=u7m2CG84BQ

## 핵심 내용
- facts가 긴 자연 텍스트 전체에 흩어져 있는 reasoning benchmark를 제안한다.
- 많은 모델이 advertised context의 10–20% 정도만 실효적으로 쓴다고 보고한다.

## 왜 CRB와 관련 있는가
- CRB도 긴 history 안에서 마지막 target reasoning이 흔들리는 문제를 본다.
- 특히 단순 retrieval이 아니라 reasoning degradation과 연결된다는 점에서 유사한 문제의식을 가진다.

## CRB와의 차이
- BABILong은 synthetic reasoning tasks + long natural background text다.
- CRB는 이미 검증된 benchmark items를 재사용하고, dummy-turn accumulation으로 interference를 만든다.

## CRB 논문에서 어떻게 쓰면 좋은가
- “BABILong은 extremely long contexts에서 reasoning degradation을 보여주고, CRB는 훨씬 짧아도 accumulated conversational history만으로 degradation이 생길 수 있음을 보여준다”고 쓰면 좋다.

## 우리에게 주는 시사점
- CRB의 강점은 million-token scale이 아니라,
- 더 짧은 realistic benchmark setting에서도 interference를 보인다는 점이다.
