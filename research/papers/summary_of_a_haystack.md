# Summary of a Haystack: A Challenge to Long-Context LLMs and RAG Systems

- Citation: Philippe Laban, Alexander Fabbri, Caiming Xiong, Chien-Sheng Wu. 2024.
- Venue: EMNLP 2024
- Source: https://aclanthology.org/2024.emnlp-main.552/

## 핵심 내용
- long-context evaluation에서 simple needle-in-a-haystack만으로는 부족하다고 주장한다.
- summarization + citation 기반의 more realistic long-context benchmark를 제안한다.

## 왜 CRB와 관련 있는가
- CRB도 “현실적인 long-context failure”를 보려는 시도라는 점에서 가깝다.
- 특히 단순 retrieval보다 더 downstream-like evaluation protocol이 필요하다는 문제의식이 같다.

## CRB와의 차이
- SummHay는 summarization과 citation quality를 본다.
- CRB는 summary quality가 아니라 **final target accuracy** 를 본다.

## CRB 논문에서 어떻게 쓰면 좋은가
- CRB는 “realistic long-context evaluation” 흐름 안에 놓되,
- output target이 free-form summary가 아니라 benchmark correctness라는 점을 강조한다.

## 우리에게 주는 시사점
- long-context benchmark는 복잡해질수록 재현성이 떨어질 수 있다.
- CRB는 target-only scoring으로 evaluation을 더 단순하고 재현 가능하게 유지할 수 있다.
