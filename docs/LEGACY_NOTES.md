# LEGACY NOTES

- Date: 2026-03-11

## Observed legacy structure
- `Legacy/` currently holds the only visible CRB code/config/test/docs tree.
- Existing run logs/configs in `Legacy/` indicate prior smoke/mini experimentation.

## Current handling rule
- Do not delete or hide `Legacy/` yet.
- First determine whether each legacy path should be:
  1. promoted to active root,
  2. wrapped/referenced as legacy support, or
  3. retired later with explicit replacement.

## Immediate questions
- Is `Legacy/src/crb` still the canonical implementation?
- Which legacy configs are still trustworthy for March 11, 2026 pilot runs?
- Which legacy docs should be merged into root `docs/`?

## New observations from worker-4 smoke prep
- The repo-root environment is still not import-ready for CRB: `/data_x/aa007878/projects/crb/.conda/envs/crb/bin/python` cannot import `crb` from the repo root unless `PYTHONPATH=Legacy/src` (or an equivalent packaging/install fix) is supplied.
- A fresh real GPQA smoke retry from `Legacy/` still fails offline at dataset load time: `datasets.load_dataset("Idavidrein/gpqa")` could not reach the Hugging Face Hub on 2026-03-11, so the current config is not yet self-contained for network-restricted reruns.
- Cached Hugging Face artifacts exist under `/mnt/raid6/aa007878/.cache/huggingface`, but the current GPQA path is still not locally reproducible through the existing `load_dataset(...)` call.
- The current cycle therefore has a verified local fixture smoke path, but not yet a freshly re-run real-dataset GPQA smoke from the active root/Legacy handoff.

## Leader follow-up
- Root now uses a symlink bridge into `Legacy/` for `src/`, `configs/`, `scripts/`, `tests/`, and `data/`.
- Two fresh GPQA reruns now exist for this cycle after unsandboxed access was allowed:
  - `run-20260311T053304Z-f40cce6c`
  - `run-20260311T054045Z-c4316b30`
- The remaining reproducibility issue is therefore not “can GPQA run,” but “can it rerun without external access / approval on a cold cache.”
