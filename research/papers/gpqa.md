# GPQA: A Graduate-Level Google-Proof Q&A Benchmark

- Citation: David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang, Julien Dirani, Julian Michael, Samuel R. Bowman. 2024.
- Venue: COLM 2024
- Source: https://openreview.net/forum?id=Ti67584b98

## 핵심 내용
- biology / physics / chemistry의 448개 전문가 작성 객관식 문제를 제시한다.
- highly skilled non-experts도 웹 검색을 써서 낮은 점수를 내도록 설계된 “Google-proof” benchmark다.

## 왜 CRB와 관련 있는가
- CRB의 가장 중요한 pilot / paper-message dataset이다.
- 과학 도메인에서 same-domain / cross-domain dummy interference를 보기 좋다.

## CRB와의 차이
- GPQA 원 논문은 benchmark 난이도와 scalable oversight relevance를 강조한다.
- CRB는 GPQA 문제를 이용해 **앞선 conversation history가 마지막 과학 문제 정답률에 미치는 간섭** 을 측정한다.

## CRB 논문에서 어떻게 쓰면 좋은가
- GPQA는 “어려운 target problem” 축으로 쓰고,
- CRB는 그 어려운 target이 **history contamination에 얼마나 더 취약해지는지** 를 보여주는 benchmark layer라고 설명하면 좋다.

## 우리에게 주는 시사점
- same-domain dummy 효과를 보이기 가장 좋은 dataset다.
- 현재 실험에서도 thinking-on branch의 format failure가 잘 드러나므로, answer emission / parsing 분석에 핵심 데이터다.
