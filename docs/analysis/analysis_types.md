# Analysis Types

These analysis types define **what** to produce, not just **how** to compute it.

## A. Operator status check
- **Goal:** answer "what is the current winner and why?"
- **Typical inputs:** scoreboard slice table + decomposition table.
- **Typical output:** 5-10 bullet summary for the next execution decision.

## B. Mechanism analysis
- **Goal:** explain *why* performance changes under accumulated history.
- **Typical inputs:** paired deltas and mechanism comparison table.
- **Typical output:** short memo on self/oracle, same/cross, and multi-turn/flattened gaps.

## C. Format robustness analysis
- **Goal:** separate reasoning failure from answer-emission failure.
- **Typical inputs:** parsed/invalid counts + error buckets.
- **Typical output:** concise taxonomy with the dominant failure modes.

## D. Replication/transfer analysis
- **Goal:** check whether the current winner holds across reruns or datasets.
- **Typical inputs:** repeated runs or same-control runs on another dataset.
- **Typical output:** go/no-go note for promoting a control from provisional to default.

## E. Paper-draft package
- **Goal:** prepare reusable tables/figures for a related-work or results section.
- **Typical inputs:** stable aggregate tables, one clean plot per claim, and references from `research/`.
- **Typical output:** figure-ready notes with consistent terminology.

## Recommended order

1. Operator status check
2. Format robustness analysis
3. Mechanism analysis
4. Replication/transfer analysis
5. Paper-draft package
