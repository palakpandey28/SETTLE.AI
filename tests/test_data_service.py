from data_service import get_transaction


def test_existing_transaction():
    result = get_transaction("TX0096")

    assert result is not None
    assert result["transaction_id"] == "TX0096"


def test_nonexistent_transaction():
    result = get_transaction("TX9999")

    assert result is None


def test_missing_ledger_record():
    # TX0096 is known to have gateway + bank data, but a mismatched
    # ledger amount. This checks the record itself isn't silently dropped.
    result = get_transaction("TX0096")

    assert result["ledger"] is not None


def test_amount_mismatch_detected():
    # TX0096 gateway/bank = 1000, ledger = 950 -> should be flagged
    result = get_transaction("TX0096")

    assert result["amount_consistent"] is False
    assert "Transaction amounts are inconsistent across systems." in result["issues"]