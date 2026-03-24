# CRB Bootstrap Workspace

CRB (Conversation-Accumulated Robustness Benchmark) turns standard single-turn benchmarks into a **multi-turn accumulated-history** evaluation setting so we can measure how earlier dummy turns interfere with the final target answer.

The repository root now has two execution lanes:

- `Legacy/` — preserved reference-only legacy experiment tree
- `src/crb_v2/` + `configs_v2/` — new integrated CRB v2 pipeline

For new execution work, use **CRB v2**.

## Start here

Read in this order when resuming work:

1. `README.md` — root navigation
2. `docs/crb_v2/README.md` — new integrated pipeline overview
3. `docs/crb_v2/BENCHMARKS_AND_SCORING.md` — benchmark/domain/type map
4. `docs/crb_v2/FAILURE_TAXONOMY.md` — failure and pool-eligibility policy
5. `docs/crb_v2/EXPERIMENT_MATRIX.md` — model/benchmark/sweep matrix
6. `CRB_EXPERIMENT_SETUP.md` — continuation rules and operating context
7. `docs/CLAIM_PROTOCOL_ALIGNMENT_20260320.md` — current claim freeze, baseline, and what counts as main-vs-secondary evidence
8. `docs/WORKFLOW_ANALYSIS.md` — how research/docs-analysis/tools/raw artifacts fit together
9. `docs/EXECUTION_STATUS.md` — current verified execution state
10. `docs/RESULTS_LOG.md` — run-by-run evidence log
11. `docs/ANALYSIS.md` — current interpretation
12. `docs/TODO_NEXT.md` — operator decision queue
13. `research/README.md` — related-work framing
14. `Legacy/README.md` — legacy runnable implementation details

For the benchmark framing itself, see `README_CRB.md`.

## Source-of-truth map

| Path | Role | Notes |
| --- | --- | --- |
| `Legacy/` | Reference-only legacy tree | Preserve old configs/artifacts; do not use it as the primary execution surface for new CRB work. |
| `src/crb_v2/`, `configs_v2/` | Canonical CRB v2 execution surface | Run the integrated baseline → pool → sweep → aggregate pipeline from here. |
| `research/` | Research framing | Paper notes, research directions, related-work buckets, and methodology extensions. |
| `docs/` | Operator-facing docs | Status, result logs, interpretation, next actions, and workflow navigation. |
| `analysis/` | Derived analysis outputs | Tables, figures, error buckets, notes, and operator-facing summaries derived from `Legacy/` artifacts. |
| `tools/` | Lightweight analysis scripts | Read-only helpers for aggregating scoreboard rows, building tables, bucketing failures, and plotting trends from `Legacy/` artifacts. |
| `results/`, `logs/` | Bootstrap leftovers / reference outputs | Do **not** treat these as the authoritative continuation artifact store; current source-of-truth remains `Legacy/results/` and `Legacy/logs/`. |
| `configs/`, `data/`, `scripts/`, `tests/` | Root bridge paths | Convenience links into `Legacy/`. |

## Workflow summary

1. **Orient** with the root/docs files listed above.
2. **Run CRB v2** via `python -m crb_v2.cli --config configs_v2/<...>.yaml` for new experiments.
3. **Use `research/`** to keep the analysis aligned with CRB's actual claim and the literature buckets it should speak to.
4. **Use `analysis/`** to decide what small tables, comparisons, and error buckets to produce next.
5. **Use `tools/`** when you want repeatable summaries from existing artifacts. The intended commands are:
   - `python -m tools.aggregate_results`
   - `python -m tools.build_tables`
   - `python -m tools.bucket_errors`
   - `python -m tools.plot_results`
6. **Inspect raw evidence** from `results_v2/` for v2 runs or `Legacy/results/` for legacy runs.
7. **Write the conclusion back** into docs-first form (`docs/ANALYSIS.md`, `docs/TODO_NEXT.md`, or `docs/WORKFLOW_ANALYSIS.md`).

## Guardrails

- Do not launch new experiments through ad hoc one-off scripts.
- Keep legacy execution in `Legacy/`, but treat CRB v2 as the canonical new runtime.
- Treat `results_v2/` as canonical raw evidence for v2 runs and `Legacy/results/` only for legacy reference runs.
- Treat `tools/` as a read-only analysis helper lane over existing artifacts.
- Avoid editing live artifact files when you only need workflow or analysis documentation.

## Operator next-step checklist

- [ ] Read `docs/CLAIM_PROTOCOL_ALIGNMENT_20260320.md` before interpreting any new rows.
- [ ] Use `docs/WORKFLOW_ANALYSIS.md` to map the docs/research/tools/raw-artifact flow before changing anything else.
- [ ] Refresh stale derived analysis artifacts before drawing new conclusions from `Legacy/results/summary/scoreboard.csv`.
- [ ] Compare the parserfix, strict-final, choice-only, and `/no_think` + prefill runs using the evidence already logged in `docs/`.
- [ ] Read `analysis/README.md` plus the companion notes before deciding what summary artifact to build next.
- [ ] Refresh `analysis/tables/run_inventory.csv`, `analysis/tables/summary_table.csv`, `analysis/error_buckets/error_buckets.csv`, and `analysis/figures/metric_plot.md` before writing new conclusions.
- [ ] Decide whether the two stranded GSM8K partial runs should be completed or cleanly archived.
- [ ] Only after the analysis pass is clean and the main-claim slice is fixed, schedule the next `Legacy/` follow-up run.
