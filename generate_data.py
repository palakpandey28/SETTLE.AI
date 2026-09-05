import pandas as pd
from datetime import datetime, timedelta
import random


# Make random data reproducible
random.seed(42)


# Payment methods
payment_methods = ["UPI", "CARD", "NET_BANKING", "WALLET"]

# Merchants
merchants = [
    "MERCHANT_001",
    "MERCHANT_002",
    "MERCHANT_003"
]


# Create 100 transaction IDs
transaction_ids = [
    f"TX{number:04d}"
    for number in range(1, 101)
]


# Lists to store records
gateway_records = []
bank_records = []
ledger_records = []


# Starting date and time
start_time = datetime(2026, 9, 1, 9, 0, 0)


# Generate 100 transactions
for i, transaction_id in enumerate(transaction_ids):

    # Generate a realistic transaction amount
    amount = random.choice([
        100, 250, 499, 500, 750,
        999, 1000, 1500, 2500, 5000
    ])

    # Generate transaction timestamp
    timestamp = start_time + timedelta(minutes=i * 7)


    # Decide what kind of transaction this is
    if i < 60:
        scenario = "SUCCESS"

    elif i < 70:
        scenario = "BANK_DELAY"

    elif i < 77:
        scenario = "GATEWAY_FAILURE"

    elif i < 84:
        scenario = "LEDGER_SYNC_ISSUE"

    elif i < 90:
        scenario = "MISSING_BANK"

    elif i < 95:
        scenario = "MISSING_LEDGER"

    elif i < 98:
        scenario = "AMOUNT_MISMATCH"

    else:
        scenario = "STATUS_MISMATCH"


    # -----------------------------------------
    # Create Gateway record
    # -----------------------------------------

    gateway_record = {
        "transaction_id": transaction_id,
        "gateway_transaction_id": f"GW{50000 + i + 1:05d}",
        "timestamp": timestamp,
        "amount": amount,
        "currency": "INR",
        "payment_method": random.choice(payment_methods),
        "status": "SUCCESS",
        "settlement_status": "SETTLED",
        "merchant_id": random.choice(merchants)
    }


    # -----------------------------------------
    # Create Bank record
    # -----------------------------------------

    bank_record = {
        "transaction_id": transaction_id,
        "bank_transaction_id": f"BN{70000 + i + 1:05d}",
        "timestamp": timestamp + timedelta(
            minutes=random.randint(1, 5)
        ),
        "amount": amount,
        "currency": "INR",
        "status": "SUCCESS",
        "processing_status": "PROCESSED",
        "settlement_date": (
            timestamp + timedelta(days=1)
        ).date(),
        "bank_reference": f"UTR{9000000000 + i + 1}"
    }


    # -----------------------------------------
    # Create Ledger record
    # -----------------------------------------

    ledger_record = {
        "transaction_id": transaction_id,
        "ledger_entry_id": f"LED{90000 + i + 1:05d}",
        "timestamp": timestamp + timedelta(
            minutes=random.randint(2, 10)
        ),
        "amount": amount,
        "currency": "INR",
        "entry_type": "CREDIT",
        "status": "POSTED",
        "settlement_status": "SETTLED"
    }


    # -----------------------------------------
    # Introduce problems intentionally
    # -----------------------------------------

    # 1. Bank processing delay
    if scenario == "BANK_DELAY":

        bank_record["timestamp"] = (
            timestamp + timedelta(hours=2)
        )


    # 2. Gateway failure
    elif scenario == "GATEWAY_FAILURE":

        gateway_record["status"] = "FAILED"
        gateway_record["settlement_status"] = "FAILED"

        bank_record["status"] = "FAILED"
        bank_record["processing_status"] = "FAILED"

        ledger_record = None


    # 3. Ledger synchronization issue
    elif scenario == "LEDGER_SYNC_ISSUE":

        ledger_record = None


    # 4. Missing bank transaction
    elif scenario == "MISSING_BANK":

        bank_record = None


    # 5. Missing ledger transaction
    elif scenario == "MISSING_LEDGER":

        ledger_record = None


    # 6. Amount mismatch
    elif scenario == "AMOUNT_MISMATCH":

        ledger_record["amount"] = amount - 50


    # 7. Status mismatch
    elif scenario == "STATUS_MISMATCH":

        ledger_record["status"] = "FAILED"
        ledger_record["settlement_status"] = "FAILED"


    # -----------------------------------------
    # Store the records
    # -----------------------------------------

    gateway_records.append(gateway_record)

    if bank_record is not None:
        bank_records.append(bank_record)

    if ledger_record is not None:
        ledger_records.append(ledger_record)


# -----------------------------------------
# Convert records into pandas DataFrames
# -----------------------------------------

gateway_df = pd.DataFrame(gateway_records)

bank_df = pd.DataFrame(bank_records)

ledger_df = pd.DataFrame(ledger_records)


# -----------------------------------------
# Save DataFrames as CSV files
# -----------------------------------------

gateway_df.to_csv("gateway.csv", index=False)

bank_df.to_csv("bank.csv", index=False)

ledger_df.to_csv("ledger.csv", index=False)


# -----------------------------------------
# Show confirmation
# -----------------------------------------

print("CSV files created successfully!")

print("Gateway records:", len(gateway_df))

print("Bank records:", len(bank_df))

print("Ledger records:", len(ledger_df))