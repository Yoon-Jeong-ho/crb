# TODO NEXT

- Date: 2026-03-11

## Now
- [x] Decide `Legacy/` promote-vs-wrap strategy for the root repo (`wrap` for bootstrap)
- [ ] Align root `pyproject.toml` / entrypoints with the chosen runnable path
- [x] Merge worker outputs into one consistent root bootstrap snapshot
- [x] Reflect the new GPU4 GPQA smoke in the shared run narrative

## Near-term runs
- [ ] GPQA thinking-on parser/postprocessing fallback
- [ ] One allowed multi-GPU smoke on `4,5` (or another subset of `4,5,6,7`)
- [ ] Selective generated sweep subset for `k in {0,2,4,8}`
- [ ] Expand GSM8K off/on beyond smoke scale
- [ ] Expand AIME after numeric ambiguity review

## Docs / Git hygiene
- [x] Commit root `README.md` + bootstrap docs after the team pass settles (`28e4058`)
- [x] Push bootstrap commit to `origin/main`
- [ ] Decide whether `README_CRB.md` stays historical or is updated to current GPU policy
- [ ] Keep unresolved Legacy questions captured in `docs/LEGACY_NOTES.md`
- [ ] Distinguish “historical legacy evidence” from “newly re-verified bootstrap-cycle evidence”

## Do not forget
- [ ] Existing env only: `/data_x/aa007878/projects/crb/.conda/envs/crb`
- [ ] Keep GPU usage to `4,5,6,7` only
- [ ] Until root code exists, run from `Legacy/` with `PYTHONPATH=src`
- [ ] Distinguish “code written” from “run verified”
