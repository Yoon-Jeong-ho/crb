# Legacy Reuse Notes

CRB v2 treats `Legacy/` as reference-only.
The runtime entrypoint is `src/crb_v2/`.

## Referenced ideas from legacy

- benchmark parsing patterns
- numeric / MCQ normalization patterns
- prefix-consistent dummy ordering idea
- raw artifact layout ideas

## Not reused as runtime dependencies

- `Legacy/src/crb/*` is not imported by `src/crb_v2/*`
- v2 execution does not run through legacy CLI or legacy configs
