from data_service import get_transaction
import pandas as pd


def investigate_transaction(transaction_id):

    # Get transaction data from all systems
    data = get_transaction(transaction_id)

    # Transaction does not exist anywhere
    if data is None:
        return None

    issues = []

    gateway = data["gateway"]
    bank = data["bank"]
    ledger = data["ledger"]

    # --------------------------------------------------
    # 1. CHECK MISSING RECORDS
    # --------------------------------------------------

    if gateway is None:
        issues.append("Gateway record is missing.")

    if bank is None:
        issues.append("Bank record is missing.")

    if ledger is None:
        issues.append("Ledger record is missing.")

    # --------------------------------------------------
    # 2. CHECK AMOUNT CONSISTENCY
    # --------------------------------------------------

    amounts = []

    if gateway is not None:
        amounts.append(gateway["amount"])

    if bank is not None:
        amounts.append(bank["amount"])

    if ledger is not None:
        amounts.append(ledger["amount"])

    if len(set(amounts)) > 1:
        issues.append(
            "Transaction amounts are inconsistent across systems."
        )

    # --------------------------------------------------
    # 3. CHECK GATEWAY FAILURE
    # --------------------------------------------------

    if gateway is not None:

        if gateway["status"] == "FAILED":

            issues.append(
                "Payment failed at the gateway."
            )

    # --------------------------------------------------
    # 4. CHECK BANK PROCESSING DELAY
    # --------------------------------------------------

    if gateway is not None and bank is not None:

        gateway_time = pd.to_datetime(
            gateway["timestamp"]
        )

        bank_time = pd.to_datetime(
            bank["timestamp"]
        )

        delay = bank_time - gateway_time

        if delay.total_seconds() > 3600:

            issues.append(
                "Bank processing is delayed by more than 1 hour."
            )

    # --------------------------------------------------
    # 5. CHECK GATEWAY VS BANK STATUS
    # --------------------------------------------------

    if gateway is not None and bank is not None:

        gateway_status = gateway["status"]
        bank_status = bank["status"]

        if gateway_status != bank_status:

            issues.append(
                "Transaction status is inconsistent between gateway and bank."
            )

    # --------------------------------------------------
    # 6. DETERMINE OVERALL STATUS
    # --------------------------------------------------

    if len(issues) == 0:

        overall_status = "NORMAL"

    else:

        overall_status = "ISSUE_DETECTED"

    # --------------------------------------------------
    # 7. RETURN INVESTIGATION RESULT
    # --------------------------------------------------

    return {
        "transaction_id": transaction_id,
        "overall_status": overall_status,
        "issues": issues,
        "data": data
    }