# Methodology Extensions

These are the most useful protocol extensions once the current CRB baseline is stable.

## Priority 1

### Replicate the provisional winner
- Test whether `/no_think` + prefill stays stable across another run or another dataset.

### Self vs oracle contamination gap
- Quantify how much extra degradation comes from the model's own prior answers.

### Same-domain vs cross-domain interference
- Check whether semantically aligned dummy turns hurt more than unrelated ones.

## Priority 2

### Multi-turn vs flattened control
- Separate turn-structure effects from pure length effects.

### Wrong-history control
- Compare gold/oracle history with explicitly wrong or self-generated history.

### Token-length matched control
- Hold approximate total length constant while changing turn structure.

## Priority 3

### Denser `k` grid
- Add `k=1`, `k=6`, or `k=12` only after the main slices are filled.

### Fixed generated-history transfer
- Reuse one model's generated history across models to separate self-contamination from external contaminated-history robustness.
