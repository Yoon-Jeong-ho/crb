# Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena

- Citation: Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, Ion Stoica. 2023.
- Venue: NeurIPS 2023 Datasets and Benchmarks
- Source: https://openreview.net/forum?id=uccHPGDlao

## 핵심 내용
- open-ended multi-turn assistant evaluation은 기존 benchmark로 어렵다고 본다.
- MT-Bench와 Chatbot Arena를 제안하고, strong LLM judge가 human preference와 높은 합의를 보인다고 주장한다.

## 왜 CRB와 관련 있는가
- CRB도 multi-turn setting을 다룬다.
- 하지만 MT-Bench류는 **대화 quality / preference** 를 보며, CRB는 **마지막 target correctness** 를 본다.

## CRB와의 차이
- MT-Bench: open-ended dialog evaluation
- CRB: benchmark target question under accumulated dialog history
- 즉, CRB는 preference benchmark가 아니라 **controlled interference benchmark** 다.

## CRB 논문에서 어떻게 쓰면 좋은가
- “기존 multi-turn benchmark는 대화 품질을 평가하지만, CRB는 prior turns가 downstream target accuracy를 얼마나 손상하는지 평가한다” 라고 선명하게 대비시킨다.

## 우리에게 주는 시사점
- CRB는 multi-turn benchmark로 오해되기 쉽다.
- Related Work에서 MT-Bench와 반드시 분리해서 설명해야 한다.
