from __future__ import annotations

from typing import Any

from crb.schemas import HistoryTurn, NormalizedItem, PromptConfig


LETTER_CHOICES = list("ABCDEFGHIJ")



def render_question_block(item: NormalizedItem) -> str:
    lines = [item.question.strip()]
    if item.choices:
        lines.append("")
        for index, choice in enumerate(item.choices):
            lines.append(f"{LETTER_CHOICES[index]}. {choice}")
    lines.append("")
    lines.append("Provide exactly one final answer.")
    return "\n".join(lines).strip()



def render_history_entry(turn: HistoryTurn, prompt_config: PromptConfig) -> str:
    answer = turn.normalized_answer if turn.normalized_answer is not None else "[invalid]"
    return (
        f"Question:\n{turn.question.strip()}\n\n"
        f"{prompt_config.history_answer_prefix} {answer}"
    )



def build_multi_turn_messages(
    *,
    history: list[HistoryTurn],
    target_item: NormalizedItem,
    prompt_config: PromptConfig,
) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = [{"role": "system", "content": prompt_config.system_prompt}]
    for turn in history:
        messages.append({"role": "user", "content": turn.question})
        answer = turn.normalized_answer if turn.normalized_answer is not None else "[invalid]"
        messages.append({"role": "assistant", "content": f"{prompt_config.history_answer_prefix} {answer}"})
    target_content = (
        f"{render_question_block(target_item)}\n\n{prompt_config.final_answer_instruction}"
    )
    messages.append({"role": "user", "content": target_content})
    return messages



def build_flattened_prompt(
    *,
    history: list[HistoryTurn],
    target_item: NormalizedItem,
    prompt_config: PromptConfig,
) -> str:
    chunks: list[str] = [prompt_config.system_prompt]
    if history:
        chunks.append("Previous solved questions:")
        for turn_index, turn in enumerate(history, start=1):
            chunks.append(f"[History {turn_index}]\n{render_history_entry(turn, prompt_config)}")
    chunks.append("Now solve the final target question.")
    chunks.append(render_question_block(target_item))
    chunks.append(prompt_config.final_answer_instruction)
    return "\n\n".join(chunk.strip() for chunk in chunks if chunk.strip())



def render_single_turn_prompt(item: NormalizedItem, prompt_config: PromptConfig) -> str:
    return "\n\n".join(
        [
            prompt_config.system_prompt,
            render_question_block(item),
            prompt_config.final_answer_instruction,
        ]
    )
