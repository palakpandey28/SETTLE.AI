from agent import run_agent


def test_agent(question, expected_transaction=None):
    print("\n" + "=" * 70)
    print("QUESTION:")
    print(question)
    print("=" * 70)

    try:
        result = run_agent(question)

        print("\nRESULT:")
        print(result.model_dump_json(indent=2))

        # Check transaction ID when we expect one
        if expected_transaction:
            if result.transaction_id == expected_transaction:
                print("\n✅ Transaction ID test PASSED")
            else:
                print(
                    f"\n❌ Transaction ID test FAILED"
                    f"\nExpected: {expected_transaction}"
                    f"\nGot: {result.transaction_id}"
                )

        # Basic response validation
        required_fields = [
            "status",
            "transaction_id",
            "problem",
            "explanation",
            "recommended_action",
            "confidence"
        ]

        missing_fields = []

        for field in required_fields:
            if not getattr(result, field, None):
                missing_fields.append(field)

        if not missing_fields:
            print("✅ Structured response test PASSED")
        else:
            print(
                f"❌ Structured response test FAILED"
                f"\nMissing fields: {missing_fields}"
            )

        return result

    except Exception as e:
        print("\n❌ TEST FAILED")
        print(type(e).__name__)
        print(e)
        return None


# ============================================================
# TEST 1 — NORMAL TRANSACTION
# ============================================================

test_agent(
    "Check TX0001 and tell me whether the transaction is normal.",
    expected_transaction="TX0001"
)


# ============================================================
# TEST 2 — KNOWN ISSUE
# ============================================================

test_agent(
    "Investigate TX0096 and explain why it is not settling.",
    expected_transaction="TX0096"
)


# ============================================================
# TEST 3 — NATURAL LANGUAGE
# ============================================================

test_agent(
    "Something seems wrong with payment TX0096. "
    "Please figure out what happened.",
    expected_transaction="TX0096"
)


# ============================================================
# TEST 4 — NON-EXISTENT TRANSACTION
# ============================================================

test_agent(
    "Investigate transaction TX9999.",
    expected_transaction="TX9999"
)


# ============================================================
# TEST 5 — NO TRANSACTION ID
# ============================================================

test_agent(
    "Why can a payment fail to settle?"
)


print("\n")
print("=" * 70)
print("PART 5 AGENT TESTING COMPLETED")
print("=" * 70)