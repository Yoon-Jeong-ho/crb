# CRB v2 Rebuild Plan

This document records the clean-room rebuild plan for the new CRB pipeline.

## Goal

Implement a standalone pipeline that runs, in one consistent flow:

1. single-turn baseline collection
2. parseable correct / incorrect / oracle pool construction
3. relation-aware multi-turn k-sweep
4. aggregation and shareable reporting

## New execution surface

- Runtime code: `src/crb_v2/`
- Configs: `pipeline_configs/`
- Tests: `pipeline_tests/`
- Docs: `docs/crb_v2/`
- Results: `crb_v2_results/` (default)
- Logs: `crb_v2_logs/` (default)

`Legacy/` remains reference-only.

## Stage boundaries

- `benchmarks/`: benchmark adapters, prompt formatting, extraction, scoring
- `stages/baseline.py`: single-turn baseline execution + per-item outcome capture
- `stages/pools.py`: correct / incorrect / oracle pools and global catalog
- `stages/sweep.py`: deterministic relation/provenance/k-sweep execution
- `stages/aggregate.py`: CSV/JSON/Markdown summaries
- `stages/pipeline.py`: single entrypoint orchestration

## Guardrails

- format/parse failures never enter incorrect dummy pools
- oracle turns use gold final answer only
- k-sampling is deterministic and prefix-consistent
- truncation/overflow decisions are recorded as reason codes
- new runtime must not import Legacy modules at execution time

## Legacy references explicitly allowed

Only implementation ideas are borrowed from legacy code, then re-implemented in `crb_v2`:

- normalized dataset record shape
- domain canonicalization patterns
- MCQ / numeric parsing ideas
- deterministic dummy sampling pattern
- result/pool serialization concepts
