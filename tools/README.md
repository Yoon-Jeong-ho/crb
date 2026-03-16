# CRB Tooling Lane

These scripts provide a lightweight, read-only analysis layer over the existing CRB experiment artifacts under `Legacy/results` and `Legacy/logs`.

## Scope

- Inputs are existing artifacts only.
- The scripts do **not** launch experiments or mutate live result files.
- Outputs default under `analysis/`, and each script exposes a simple path override when needed.

## Scripts

### `aggregate_results.py`
Builds a normalized run inventory by combining `Legacy/results/summary/scoreboard.csv` with the matching run JSON files.

```bash
python -m tools.aggregate_results
```

Default output:
- `analysis/tables/run_inventory.csv`

### `build_tables.py`
Builds grouped operator-friendly tables from the normalized run inventory.

```bash
python -m tools.build_tables
```

Default outputs:
- `analysis/tables/summary_table.csv`
- `analysis/tables/summary_table.md`

### `bucket_errors.py`
Buckets invalid outputs from saved run JSONs into reusable categories.

```bash
python -m tools.bucket_errors
```

Default outputs:
- `analysis/error_buckets/error_buckets.csv`
- `analysis/error_buckets/error_buckets.md`

### `plot_results.py`
Builds a dependency-light Mermaid plot from the grouped summary table.

```bash
python -m tools.plot_results
```

Default output:
- `analysis/figures/metric_plot.md`

## Suggested operator order

1. `python -m tools.aggregate_results`
2. `python -m tools.build_tables`
3. `python -m tools.bucket_errors`
4. `python -m tools.plot_results`
