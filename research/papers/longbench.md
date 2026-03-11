# LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding

- Citation: Yushi Bai, Xin Lv, Jiajie Zhang, Hongchang Lyu, Jiankai Tang, Zhidian Huang, Zhengxiao Du, Xiao Liu, Aohan Zeng, Lei Hou, Yuxiao Dong, Jie Tang, Juanzi Li. 2024.
- Venue: ACL 2024
- Source: https://aclanthology.org/2024.acl-long.172/

## 핵심 내용
- long context understanding을 위한 bilingual multi-task benchmark를 제안한다.
- single-doc QA, multi-doc QA, summarization, few-shot learning, synthetic tasks, code completion 등을 포함한다.

## 왜 CRB와 관련 있는가
- LongBench는 broad long-context benchmark의 대표 사례다.
- CRB는 이 broad setting보다 훨씬 좁지만, 원인 해석이 더 잘 되는 protocol을 제공한다.

## CRB와의 차이
- LongBench는 task variety와 long context coverage를 강조한다.
- CRB는 범용 long-context benchmark가 아니라 **standard benchmarks under dummy-turn accumulation** 이다.

## CRB 논문에서 어떻게 쓰면 좋은가
- LongBench는 “long-context benchmark landscape” reference로 인용하고,
- CRB는 그 landscape 안에서 **turn-structured contamination** 을 직접 분리하는 benchmark라고 위치시킨다.

## 우리에게 주는 시사점
- LongBench식 broad benchmark를 흉내내기보다,
- CRB는 “mechanism-isolating benchmark” 라는 정체성을 유지하는 편이 좋다.
