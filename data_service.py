import pandas as pd


# -----------------------------------------
# Load the three CSV files
# -----------------------------------------

gateway_df = pd.read_csv("gateway.csv")
bank_df = pd.read_csv("bank.csv")
ledger_df = pd.read_csv("ledger.csv")


# -----------------------------------------
# Function to get one transaction
# -----------------------------------------

def get_transaction(transaction_id):

    # -----------------------------------------
    # Search Gateway
    # -----------------------------------------

    gateway_match = gateway_df[
        gateway_df["transaction_id"] == transaction_id
    ]


    # -----------------------------------------
    # Search Bank
    # -----------------------------------------

    bank_match = bank_df[
        bank_df["transaction_id"] == transaction_id
    ]


    # -----------------------------------------
    # Search Ledger
    # -----------------------------------------

    ledger_match = ledger_df[
        ledger_df["transaction_id"] == transaction_id
    ]


    # -----------------------------------------
    # Check if transaction exists anywhere
    # -----------------------------------------

    if (
        gateway_match.empty
        and bank_match.empty
        and ledger_match.empty
    ):
        return None


    # -----------------------------------------
    # Convert Gateway result to dictionary
    # -----------------------------------------

    if gateway_match.empty:
        gateway_data = None
    else:
        gateway_data = gateway_match.iloc[0].to_dict()


    # -----------------------------------------
    # Convert Bank result to dictionary
    # -----------------------------------------

    if bank_match.empty:
        bank_data = None
    else:
        bank_data = bank_match.iloc[0].to_dict()


    # -----------------------------------------
    # Convert Ledger result to dictionary
    # -----------------------------------------

    if ledger_match.empty:
        ledger_data = None
    else:
        ledger_data = ledger_match.iloc[0].to_dict()


    # -----------------------------------------
    # Check transaction amounts
    # -----------------------------------------

    amounts = []

    if gateway_data is not None:
        amounts.append(gateway_data["amount"])

    if bank_data is not None:
        amounts.append(bank_data["amount"])

    if ledger_data is not None:
        amounts.append(ledger_data["amount"])


    # If all available amounts are the same,
    # the amounts are consistent.

    amount_consistent = len(set(amounts)) <= 1


    # -----------------------------------------
    # Create list of issues
    # -----------------------------------------

    issues = []

    if gateway_data is None:
        issues.append("Gateway record is missing.")

    if bank_data is None:
        issues.append("Bank record is missing.")

    if ledger_data is None:
        issues.append("Ledger record is missing.")

    if not amount_consistent:
        issues.append(
            "Transaction amounts are inconsistent across systems."
        )


    # -----------------------------------------
    # Create final result
    # -----------------------------------------

    result = {
        "transaction_id": transaction_id,
        "gateway": gateway_data,
        "bank": bank_data,
        "ledger": ledger_data,
        "amount_consistent": amount_consistent,
        "issues": issues
    }


    return result