from crb_v2.benchmarks.base import parse_multiple_choice, parse_numeric_boxed, parse_short_answer, parse_yes_no


def test_parse_multiple_choice_valid_and_invalid_option():
    parsed = parse_multiple_choice("Answer: B", ["x", "y", "z"])
    assert parsed.status == "parsed"
    assert parsed.normalized_answer == "B"

    invalid = parse_multiple_choice("Answer: Z", ["x", "y", "z"])
    assert invalid.status == "invalid"
    assert invalid.reason_code == "parse_failure"


def test_parse_numeric_boxed_requires_box_or_answer_line_consistency():
    parsed = parse_numeric_boxed("Work...\\nAnswer: \\boxed{42}")
    assert parsed.status == "parsed"
    assert parsed.normalized_answer == "42"

    boxed_missing = parse_numeric_boxed("The result is 42")
    assert boxed_missing.status == "invalid"
    assert boxed_missing.reason_code == "boxed_missing"


def test_parse_yes_no_and_short_answer_conflicts():
    parsed = parse_yes_no("Answer: yes")
    assert parsed.status == "parsed"
    assert parsed.normalized_answer == "yes"

    invalid = parse_yes_no("yes ... no")
    assert invalid.status == "invalid"
    assert invalid.reason_code == "conflicting_final_answers"

    short = parse_short_answer("Reasoning\\nAnswer: Blue whale")
    assert short.status == "parsed"
    assert short.normalized_answer == "blue whale"
