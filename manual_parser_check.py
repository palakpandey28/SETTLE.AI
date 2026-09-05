from transaction_parser import extract_transaction_id


questions = [
    "Why hasn't TX0001 been settled?",
    "What's wrong with TX0096?",
    "Is TX0065 successfully settled?",
    "Where is TX0096 stuck?",
    "Why are payments failing?"
]


for question in questions:
    transaction_id = extract_transaction_id(question)

    print("Question:", question)
    print("Transaction ID:", transaction_id)
    print()
    