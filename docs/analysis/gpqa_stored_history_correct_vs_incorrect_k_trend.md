# GPQA Stored-History k Trend

This note summarizes the `Qwen/Qwen3-1.7B` GPQA `stored_history` comparison using
`same_domain` dummy histories drawn from the model's own single-turn pools.

Compared lanes:
- `correct` pool
- `incorrect` pool

Compared settings:
- thinking `off`
- thinking `on` with `/no_think + prefill`

`k = 2, 4, 8, 16`

## Thinking off

| k | correct acc | incorrect acc | acc gap (correct - incorrect) | correct FF | incorrect FF |
| --- | --- | --- | --- | --- | --- |
| 2 | 0.2813 | 0.2768 | +0.0045 | 0.0089 | 0.0089 |
| 4 | 0.2634 | 0.2946 | -0.0313 | 0.0000 | 0.0022 |
| 8 | 0.2656 | 0.2455 | +0.0201 | 0.0000 | 0.0022 |
| 16 | 0.3080 | 0.2902 | +0.0179 | 0.0000 | 0.0000 |

### Readout

- The trend is **not monotonic** in either lane.
- The incorrect pool is not uniformly worse.
- At larger `k` (`8`, `16`), the correct pool is better on accuracy and at least as stable on format.
- From `k=2 -> 16`, both lanes improve slightly in accuracy and improve in format stability.

## Thinking on

| k | correct acc | incorrect acc | acc gap (correct - incorrect) | correct FF | incorrect FF |
| --- | --- | --- | --- | --- | --- |
| 2 | 0.2612 | 0.2589 | +0.0022 | 0.0246 | 0.0201 |
| 4 | 0.2768 | 0.2768 | 0.0000 | 0.0379 | 0.0246 |
| 8 | 0.2567 | 0.2656 | -0.0089 | 0.0469 | 0.0313 |
| 16 | 0.2522 | 0.2522 | 0.0000 | 0.0290 | 0.0268 |

### Readout

- The trend is also **not monotonic**.
- Accuracy is nearly flat between the correct and incorrect pools.
- Format-failure rates are consistently higher than in the thinking-off comparison.
- From `k=2 -> 16`, both lanes lose a little accuracy and become slightly less format-stable overall.

## Short conclusion

1. `k` does matter, but the effect is not a simple monotonic degradation curve in these stored-history GPQA runs.
2. Pool correctness alone is not the dominant factor at every `k`.
3. The clearer pattern is that the thinking-on lane remains more format-sensitive than the thinking-off lane.
4. A cautious claim is:
   - stored-history pool correctness has a **modest**, `k`-dependent effect
   - thinking mode and output stability appear to be larger drivers than pool correctness by itself
