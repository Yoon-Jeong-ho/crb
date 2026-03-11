# Measuring Massive Multitask Language Understanding (MMLU)

- Citation: Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, Jacob Steinhardt. 2021.
- Venue: ICLR 2021
- Source: https://openreview.net/forum?id=d7KBjmI3GmQ

## 핵심 내용
- 57개 과목의 객관식 문제로 모델의 broad academic/professional understanding을 측정한다.
- 큰 모델도 전문가 수준과는 여전히 거리가 있고, 어떤 과목에서는 거의 random 수준이다.

## 왜 CRB와 관련 있는가
- CRB가 사용하는 핵심 anchor benchmark 중 하나다.
- CRB는 MMLU를 버리지 않고, **single-turn benchmark를 accumulated-history setting으로 다시 본다**.

## CRB와의 차이
- MMLU는 원래 single-turn multiple-choice benchmark다.
- CRB는 같은 문제를 유지하되, 앞에 dummy turn을 누적하고 **마지막 target만 score** 한다.

## CRB 논문에서 어떻게 쓰면 좋은가
- MMLU는 “표준 benchmark의 breadth”를 보장하는 reference로 둔다.
- novelty는 MMLU dataset이 아니라 **CRB evaluation protocol** 에 있다고 분명히 적는다.

## 우리에게 주는 시사점
- MMLU-family는 GPQA/GSM8K/AIME보다 “일반 지식 anchor” 역할에 더 적합하다.
- same/cross-domain 간섭 분석에서 broad subject/domain 구분이 특히 중요하다.
