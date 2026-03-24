# Failure Taxonomy

## Reason codes

- `parse_failure`
- `format_failure`
- `boxed_missing`
- `invalid_option_choice`
- `empty_output`
- `conflicting_final_answers`
- `context_overflow`
- `truncation_applied`
- `skipped_due_to_budget`
- `invalid_generation`
- `runtime_exception`
- `insufficient_dummy_pool`

## Pool eligibility

A baseline item is eligible for the incorrect pool only if:

1. `parse_status == parsed`
2. `scoreable == true`
3. `is_correct == false`
4. `reason_codes` do not contain format / parse failure codes

This keeps malformed outputs out of the incorrect dummy pool.
