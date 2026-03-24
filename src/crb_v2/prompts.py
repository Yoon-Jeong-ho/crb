from __future__ import annotations

from crb_v2.types import HistoryTurn, NormalizedExample



def render_question_block(example: NormalizedExample) -> str:
    lines = [example.question.strip()]
    if example.choices:
        lines.append("")
        for idx, choice in enumerate(example.choices):
            lines.append(f"{chr(ord('A') + idx)}. {choice}")
    lines.append("")
    lines.append("Provide exactly one final answer.")
    return "\n".join(lines).strip()



def build_single_turn_prompt(example: NormalizedExample, *, system_prompt: str, final_answer_instruction: str) -> str:
    return "\n\n".join([system_prompt.strip(), render_question_block(example), final_answer_instruction.strip()]).strip()



def build_multi_turn_prompt(
    example: NormalizedExample,
    history: list[HistoryTurn],
    *,
    system_prompt: str,
    final_answer_instruction: str,
    history_answer_prefix: str,
) -> str:
    chunks = [system_prompt.strip()]
    if history:
        chunks.append("Previous solved questions:")
        for index, turn in enumerate(history, start=1):
            answer = turn.answer if turn.answer is not None else "[invalid]"
            chunks.append(
                f"[History {index}]\nQuestion:\n{turn.question.strip()}\n\n{history_answer_prefix} {answer}"
            )
    chunks.append("Now solve the final target question.")
    chunks.append(render_question_block(example))
    chunks.append(final_answer_instruction.strip())
    return "\n\n".join(chunk for chunk in chunks if chunk).strip()
