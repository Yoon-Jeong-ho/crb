# Methodology Extensions

These are the most useful protocol extensions once the current CRB baseline is stable.
Each extension keeps the benchmark items fixed and changes only the evaluation setup or analysis lens.

## Priority 1 — strengthen the current story

### 1. Replicate the provisional winner
- **Question:** Does `/no_think` + prefill stay stable across another run or dataset?
- **Why first:** It tests whether the current best control is real or just small-sample noise.
- **Minimum artifact:** one repeat on GPQA or one transfer run on GSM8K/MMLU.

### 2. Self vs oracle contamination gap
- **Question:** How much extra degradation comes from the model's own prior answers?
- **Why it matters:** This is the cleanest evidence for history contamination rather than pure context length.
- **Recommended report:** paired table by dataset, `k`, and domain bucket.

### 3. Same-domain vs cross-domain interference
- **Question:** Are semantically aligned dummy turns worse than unrelated ones?
- **Why it matters:** A larger same-domain drop supports the semantic-interference claim.
- **Recommended report:** accuracy delta and format-failure delta side by side.

## Priority 2 — extend mechanism coverage

### 4. Multi-turn vs flattened control
- **Question:** Is the degradation driven by turn structure, not just extra tokens?
- **Recommended readout:** paired deltas with token counts noted when available.

### 5. Wrong-history control
- **Question:** How different is gold/oracle history from explicitly wrong or self-generated history?
- **Recommended use:** follow the same target set so the failure mechanism stays comparable.

### 6. Token-length matched control
- **Question:** If total length is similar, does turn structure still hurt?
- **Recommended use:** only after the primary CRB slices are well populated.

## Priority 3 — optional extensions

### 7. Denser `k` grid
- Add `k=1` for early degradation onset or `k=6/12` for smoother curves.

### 8. Fixed generated-history transfer
- Reuse one model's generated history across models to separate self-contamination from external contaminated history robustness.

## What not to do yet

- Do not add many new axes before the current winner is replicated.
- Do not treat format-only improvements as complete wins if accuracy drops.
- Do not replace the main CRB story with thinking on/off; keep it as a secondary axis.
