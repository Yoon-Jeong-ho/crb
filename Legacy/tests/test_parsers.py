from crb.evaluation.parsers import normalize_numeric_string, parse_mcq_answer, parse_numeric_answer


def test_parse_mcq_strict():
    parsed = parse_mcq_answer("Reasoning\nAnswer: c")
    assert parsed.status == "parsed"
    assert parsed.normalized_answer == "C"


def test_parse_numeric_fraction_normalization():
    parsed = parse_numeric_answer("Work\nAnswer: 0.5")
    assert parsed.status == "parsed"
    assert parsed.normalized_answer == "1/2"
    assert normalize_numeric_string("1/2") == "1/2"


def test_parse_mcq_reasoning_phrase():
    parsed = parse_mcq_answer("Long reasoning... the best choice is B because it dominates the uncertainty scale.")
    assert parsed.status == "parsed"
    assert parsed.normalized_answer == "B"
