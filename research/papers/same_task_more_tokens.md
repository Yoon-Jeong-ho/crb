# Same Task, More Tokens: the Impact of Input Length on the Reasoning Performance of Large Language Models

- Citation: Mosh Levy, Alon Jacoby, Yoav Goldberg. 2024.
- Venue: ACL 2024 (Outstanding Paper)
- Source: https://aclanthology.org/2024.acl-long.818/

## 핵심 내용
- 같은 sample에 padding만 늘려 input length 효과를 분리한다.
- 모델 reasoning 성능이 technical max보다 훨씬 짧은 길이에서부터 이미 떨어질 수 있음을 보인다.

## 왜 CRB와 관련 있는가
- CRB도 k와 history 누적으로 context가 길어질수록 마지막 target이 흔들리는 현상을 본다.
- 이 논문은 “길이 자체의 효과”를 분리하는 reference다.

## CRB와의 차이
- Same Task, More Tokens는 padding 기반 length control이다.
- CRB는 dummy question-answer turn이 누적되는 **semantically meaningful history** 를 넣는다.

## CRB 논문에서 어떻게 쓰면 좋은가
- “길이 자체도 중요하지만, CRB는 그 위에 semantic/turn-structured interference를 본다”는 식으로 차별화한다.

## 우리에게 주는 시사점
- 가능하면 token-length matched control을 추가하는 것이 좋다.
- 그러면 CRB가 단순 length effect만 보는 것이 아님을 더 강하게 주장할 수 있다.
