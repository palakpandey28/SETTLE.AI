from transaction_parser import extract_transaction_id


def test_valid_transaction_id():
    assert extract_transaction_id(
        "Why is TX0096 not settling?"
    ) == "TX0096"


def test_no_transaction_id():
    assert extract_transaction_id(
        "Why are payments failing?"
    ) is None


def test_lowercase_transaction_id():
    assert extract_transaction_id(
        "why is tx0096 stuck?"
    ) == "TX0096"


def test_malformed_question_with_id():
    assert extract_transaction_id(
        "TX0096 ??? $$$"
    ) == "TX0096"