# RULER: What's the Real Context Size of Your Long-Context Language Models?

- Citation: Cheng-Ping Hsieh, Simeng Sun, Samuel Kriman, Shantanu Acharya, Dima Rekesh, Fei Jia, Yang Zhang, Boris Ginsburg. 2024.
- Venue: COLM 2024 / arXiv 2024
- Source: https://arxiv.org/abs/2404.06654

## 핵심 내용
- vanilla needle-in-a-haystack는 long-context understanding의 매우 얕은 형태만 본다고 비판한다.
- 더 복잡한 synthetic tasks로 구성된 RULER를 제안하고, claim된 context size 대비 실제 성능 저하를 보여준다.

## 왜 CRB와 관련 있는가
- CRB도 “advertised context window != robust reasoning under long history” 메시지와 연결된다.
- 다만 CRB는 synthetic retrieval이 아니라 **real benchmark targets + conversational history** 를 쓴다.

## CRB와의 차이
- RULER는 synthetic stress test다.
- CRB는 standard evaluation tasks 위에 얹는 protocol이다.
- 그래서 CRB는 더 현실적인 benchmark transferability를 가진다.

## CRB 논문에서 어떻게 쓰면 좋은가
- RULER는 “long-context stress test” reference,
- CRB는 “benchmark-grounded interference protocol” reference로 구분한다.

## 우리에게 주는 시사점
- CRB도 장기적으로 synthetic task 없이 실제 benchmark items만으로 long-context robustness를 논할 수 있다는 장점이 있다.
