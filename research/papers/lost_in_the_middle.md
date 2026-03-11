# Lost in the Middle: How Language Models Use Long Contexts

- Citation: Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang. 2024.
- Venue: TACL 2024
- Source: https://aclanthology.org/2024.tacl-1.9/

## 핵심 내용
- relevant information의 위치가 바뀌면 성능이 크게 달라진다.
- 특히 시작/끝보다 middle에서 성능이 더 떨어지는 position bias를 보인다.

## 왜 CRB와 관련 있는가
- CRB도 긴 history가 누적되면 마지막 target이 앞선 context 속에 묻히는 현상을 측정한다.
- 다만 CRB는 단순 위치 효과가 아니라 **turn-structured accumulated interference** 까지 본다.

## CRB와의 차이
- Lost in the Middle은 주로 long input에서 relevant evidence 위치 효과를 본다.
- CRB는 evidence retrieval이 아니라 **앞선 QA turn 자체가 오염 source** 가 된다.

## CRB 논문에서 어떻게 쓰면 좋은가
- “우리는 long-context failure를 단순 위치 편향에서 한 단계 더 나아가, conversationally accumulated interference로 본다”고 연결하면 좋다.

## 우리에게 주는 시사점
- multi_turn vs flattened 비교는 꼭 넣어야 한다.
- token length control을 두면 turn structure effect를 더 강하게 주장할 수 있다.
