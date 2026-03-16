# CRB Bootstrap Workspace

CRB (Conversation-Accumulated Robustness Benchmark) turns standard single-turn benchmarks into a **multi-turn accumulated-history** evaluation setting so we can measure how earlier dummy turns interfere with the final target answer.

The repository root is currently a **documentation and workflow bridge** around the runnable `Legacy/` experiment tree.

## Start here

Read in this order when resuming work:

1. `README.md` — root navigation
2. `CRB_EXPERIMENT_SETUP.md` — continuation rules and operating context
3. `docs/WORKFLOW_ANALYSIS.md` — how research/docs-analysis/tools/raw artifacts fit together
4. `docs/EXECUTION_STATUS.md` — current verified execution state
5. `docs/RESULTS_LOG.md` — run-by-run evidence log
6. `docs/ANALYSIS.md` — current interpretation
7. `docs/TODO_NEXT.md` — operator decision queue
8. `research/README.md` — related-work framing
9. `research/directions.md` — current analysis questions to prioritize
10. `research/related_work_buckets.md` — literature buckets to cite against
11. `research/methodology_extensions.md` — follow-up extension ideas
12. `docs/analysis/README.md` — analysis lane index
13. `Legacy/README.md` — runnable implementation details

For the benchmark framing itself, see `README_CRB.md`.

## Source-of-truth map

| Path | Role | Notes |
| --- | --- | --- |
| `Legacy/` | Canonical runnable tree | Execute code/config/tests from here. Raw artifacts live under `Legacy/results/` and `Legacy/logs/`. |
| `research/` | Research framing | Paper notes, research directions, related-work buckets, and methodology extensions. |
| `docs/` | Operator-facing docs | Status, result logs, interpretation, next actions, and workflow navigation. |
| `analysis/` | Derived analysis outputs | Tables, figures, error buckets, notes, and operator-facing summaries derived from `Legacy/` artifacts. |
| `tools/` | Lightweight analysis scripts | Read-only helpers for aggregating scoreboard rows, building tables, bucketing failures, and plotting trends from `Legacy/` artifacts. |
| `results/`, `logs/` | Bootstrap leftovers / reference outputs | Do **not** treat these as the authoritative continuation artifact store; current source-of-truth remains `Legacy/results/` and `Legacy/logs/`. |
| `configs/`, `data/`, `scripts/`, `tests/` | Root bridge paths | Convenience links into `Legacy/`. |

## Workflow summary

1. **Orient** with the root/docs files listed above.
2. **Use `research/`** to keep the analysis aligned with CRB's actual claim and the literature buckets it should speak to.
3. **Use `analysis/`** to decide what small tables, comparisons, and error buckets to produce next.
4. **Use `tools/`** when you want repeatable summaries from existing artifacts. The intended commands are:
   - `python -m tools.aggregate_results`
   - `python -m tools.build_tables`
   - `python -m tools.bucket_errors`
   - `python -m tools.plot_results`
5. **Inspect raw evidence** from `Legacy/results/` and `Legacy/logs/`.
6. **Write the conclusion back** into docs-first form (`docs/ANALYSIS.md`, `docs/TODO_NEXT.md`, or `docs/WORKFLOW_ANALYSIS.md`).

## Guardrails

- Do not launch new experiments from the root workflow lane.
- Keep the runnable implementation in `Legacy/`.
- Treat `Legacy/results/` and `Legacy/logs/` as canonical raw evidence.
- Treat `tools/` as a read-only analysis helper lane over existing artifacts.
- Avoid editing live artifact files when you only need workflow or analysis documentation.

## Operator next-step checklist

- [ ] Use `docs/WORKFLOW_ANALYSIS.md` to map the docs/research/tools/raw-artifact flow before changing anything else.
- [ ] Compare the parserfix, strict-final, choice-only, and `/no_think` + prefill runs using the evidence already logged in `docs/`.
- [ ] Read `analysis/README.md` plus the companion notes before deciding what summary artifact to build next.
- [ ] Refresh `analysis/tables/run_inventory.csv`, `analysis/tables/summary_table.csv`, `analysis/error_buckets/error_buckets.csv`, and `analysis/figures/metric_plot.md` before writing new conclusions.
- [ ] Decide whether the combined constrained + `/no_think` + prefill config should remain a fallback or be retired.
- [ ] Only after the analysis pass is clean, schedule the next `Legacy/` follow-up run or dataset extension.
