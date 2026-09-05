import json
from unittest.mock import MagicMock, patch

import agent


def make_function_call_step(call_id, name, arguments):
    step = MagicMock()
    step.type = "function_call"
    step.id = call_id
    step.name = name
    step.arguments = arguments
    return step


def test_agent_calls_get_transaction_with_correct_id():
    fake_transaction_data = {
        "transaction_id": "TX0001",
        "gateway": {"amount": 100, "status": "SUCCESS"},
        "bank": {"amount": 100, "status": "SUCCESS"},
        "ledger": {"amount": 100, "status": "POSTED"},
        "amount_consistent": True,
        "issues": []
    }

    mock_tool = MagicMock(return_value=fake_transaction_data)

    fake_investigation = {
        "transaction_id": "TX0001",
        "overall_status": "NORMAL",
        "issues": [],
        "data": fake_transaction_data
    }

    # First fake Gemini response: it asks to call get_transaction
    first_interaction = MagicMock()
    first_interaction.id = "interaction_1"
    first_interaction.steps = [
        make_function_call_step(
            "call_1",
            "get_transaction",
            json.dumps({"transaction_id": "TX0001"})
        )
    ]

    # Second fake Gemini response: the final structured answer
    second_interaction = MagicMock()
    second_interaction.steps = []
    second_interaction.output_text = json.dumps({
        "status": "NORMAL",
        "transaction_id": "TX0001",
        "problem": "None",
        "explanation": "All records match.",
        "recommended_action": "No action needed.",
        "confidence": "95%"
    })

    with patch.object(
        agent.client.interactions, "create",
        side_effect=[first_interaction, second_interaction]
    ), patch.dict(agent.available_tools, {"get_transaction": mock_tool}), \
       patch("agent.investigate_transaction", return_value=fake_investigation):

        result = agent.run_agent("Why is TX0001 not settling?", "TX0001")

        # Confirms the agent used the transaction ID extracted by
        # Python, not something Gemini might have guessed independently.
        mock_tool.assert_called_once_with("TX0001")

        assert result.transaction_id == "TX0001"
        assert result.status == "NORMAL"