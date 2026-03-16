# Analysis Methods

Use these methods to turn existing CRB artifacts into small, decision-oriented summaries.

## 1. Scoreboard slice table
- **Input:** `Legacy/results/summary/scoreboard.csv`
- **Output:** compact table grouped by scoreboard fields such as `dataset`, `evaluation_mode`, `history_mode`, `dummy_type`, `k`, and `thinking_mode`.
- **Use when:** you need the fastest status snapshot.
- **Starter columns:** `run_id`, `dataset`, `evaluation_mode`, `history_mode`, `dummy_type`, `k`, `thinking_mode`, `num_items`, `accuracy`, `format_failure_rate`, `result_json_path`.

## 2. Item-level paired delta
- **Input:** matching run JSON files for the same target items; use `per_item_results`.
- **Output:** per-item `baseline -> treatment` change table.
- **Use when:** you need to show that the same questions degrade as history accumulates.
- **Key columns:** target id, baseline correctness, treatment correctness, delta, format-valid flag.

## 3. Accuracy vs format-failure decomposition
- **Input:** scoreboard rows plus `metrics.accuracy`, `metrics.format_failure_rate`, `metrics.parsed_count`, and `metrics.invalid_count` from the run JSON.
- **Output:** one table with accuracy, parsed rate, invalid count, and a short interpretation.
- **Use when:** a control improves formatting but may hide a reasoning regression.

## 4. Error bucketing
- **Input:** invalid outputs from `per_item_results` plus matching logs if needed.
- **Output:** counts for categories such as `no_final_answer`, `multiple_answers`, `reasoning_only`, `malformed_numeric`, `other`.
- **Use when:** parser or prompting changes are under discussion.
- **Default rule:** assign one primary bucket per item so totals stay easy to audit.
- **Practical order:** check for missing final answer first, then multiple answers, then reasoning-only text, then malformed numeric output, then `other`.

## 5. Mechanism comparison table
- **Input:** aligned scoreboard/run slices across `self/oracle`, `same/cross`, and `multi_turn/flattened`.
- **Output:** small matrix of gap values.
- **Use when:** writing the paper/story claim rather than a raw run log.

## 6. Trend plots
- **Input:** aggregated table with consistent axis names.
- **Output:** line or bar plots over `k`, split by dataset or mechanism.
- **Use when:** enough rows exist to show a stable pattern.
- **Rule:** keep plots sparse; one figure should answer one question.

## 7. Bootstrap or uncertainty summary
- **Input:** item-level correctness table.
- **Output:** confidence interval or resampled win-rate summary.
- **Use when:** pilot runs are small and the comparison could be noisy.

## Minimal analysis order

1. Build a scoreboard slice table.
2. Add accuracy vs format-failure decomposition.
3. Run paired deltas for the most important comparison.
4. Bucket a small number of invalid outputs.
5. Plot only if the table already tells a coherent story.
