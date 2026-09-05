from investigation_service import investigate_transaction


def test_known_issue_transaction():
    # TX0096: amount mismatch (1000 vs 950) + status mismatch
    result = investigate_transaction("TX0096")

    assert result is not None
    assert result["overall_status"] == "ISSUE_DETECTED"
    assert len(result["issues"]) > 0


def test_amount_mismatch_flagged():
    result = investigate_transaction("TX0096")

    assert "Transaction amounts are inconsistent across systems." in result["issues"]


def test_nonexistent_transaction_returns_none():
    result = investigate_transaction("TX9999")

    assert result is None


def test_normal_transaction_has_no_issues():
    # TX0001 is in the first 60 transactions, which are all SUCCESS
    result = investigate_transaction("TX0001")

    assert result is not None
    assert result["overall_status"] == "NORMAL"
    assert result["issues"] == []
    