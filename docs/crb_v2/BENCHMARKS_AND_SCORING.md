# Benchmark / Domain / Type / Scoring Map

| Benchmark key | Domain | Type | Default HF path | Default split | Scoring rule |
| --- | --- | --- | --- | --- | --- |
| `gsm8k` | math | `numeric_boxed` | `openai/gsm8k` / `main` | `test` | numeric normalization from boxed or answer line |
| `math500` | math | `numeric_boxed` | `HuggingFaceH4/MATH-500` | `test` | numeric normalization from boxed or answer line |
| `gpqa` | science | `multiple_choice` | `Idavidrein/gpqa` | `train` | final option letter |
| `arc_challenge` | science | `multiple_choice` | `allenai/ai2_arc` / `ARC-Challenge` | `test` | final option letter |
| `mmlu_pro` | general_knowledge | `multiple_choice` | `TIGER-Lab/MMLU-Pro` | `test` | final option letter |
| `mmlu_redux_2` | general_knowledge | `multiple_choice` | `edinburgh-dawg/mmlu-redux-2.0` | `test` | final option letter |
| `hellaswag` | commonsense | `completion_choice` | `Rowan/hellaswag` | `validation` | completion option letter |
| `piqa` | commonsense | `multiple_choice` | `piqa` | `validation` | final option letter |
| `boolq` | factual_reading | `yes_no` | `google/boolq` | `validation` | yes/no extraction |
| `truthfulqa_mc` | factual_reading | `multiple_choice` | `truthfulqa/truthful_qa` / `multiple_choice` | `validation` | final option letter |

## Extraction rules

- `multiple_choice` / `completion_choice`: final option letter `A..J`
- `numeric_boxed`: prefer `\boxed{...}`, fallback to `Answer:` line numeric normalization
- `yes_no`: extract exactly one of `yes` / `no`
- `short_answer`: normalize final `Answer:` line or final non-empty line

## Pool provenance

- `model_correct`: parsed + scoreable + correct baseline outputs
- `model_incorrect`: parsed + scoreable + incorrect baseline outputs
- `oracle`: gold final answer only
