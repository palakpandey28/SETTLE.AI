import re


def extract_transaction_id(question):
    pattern = r"\bTX\d{4}\b"

    match = re.search(pattern, question.upper())

    if match:
        return match.group(0)

    return None