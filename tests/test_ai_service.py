import pytest
from ai_service import analyze_transaction
test_transaction = {
    "transaction_id": "TX0096",
    "gateway": {
        "transaction_id": "TX0096",
        "amount": 1000,
        "currency": "INR",
        "status": "SUCCESS"
    },
    "bank": {
        "transaction_id": "TX0096",
        "amount": 1000,
        "currency": "INR",
        "status": "SUCCESS"
    },
    "ledger": {
        "transaction_id": "TX0096",
        "amount": 950,
        "currency": "INR",
        "status": "POSTED"
    }
}
def test_ai_analysis_tx0096():
    result = analyze_transaction(test_transaction)
    print("\nAI ANALYSIS")
    print("--------------------")
    print("Status:", result.status)
    print("Problem:", result.problem)
    print("Explanation:", result.explanation)
    print("Recommended Action:", result.recommended_action)
    print("Confidence:", result.confidence)
    assert result.status is not None