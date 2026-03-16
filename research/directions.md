# Research Directions

These are the highest-value research questions to keep visible while CRB execution continues.

## Primary questions

1. How much does accumulated dummy history degrade the final target answer as `k` grows?
2. Is the degradation stronger in `multi_turn` than in `single_turn_flattened`?
3. Does `self_history` contaminate more than `oracle_history`?
4. Is `same_domain` history more harmful than `cross_domain` history?

## Secondary questions

1. How much of the degradation is reasoning loss versus final-answer format failure?
2. When does thinking on/off change the interpretation rather than only the answer surface?
3. Which benchmark families are most sensitive to accumulated interference?

## Immediate research priorities

1. Finish the best-covered CRB slices before adding new axes.
2. Build paired item-level comparisons instead of relying only on aggregate accuracy.
3. Separate invalid-output behavior from true reasoning failure.
4. Keep the main claim focused on accumulated-history interference rather than generic long-context robustness.
