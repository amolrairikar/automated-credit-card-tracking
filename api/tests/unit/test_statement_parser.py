import os
import json
from unittest.mock import patch, MagicMock

import pytest
from openai import OpenAIError

from api.utils.statement_parser import extract_statement_details


@patch("api.utils.statement_parser.remove_pii_columns")
@patch("api.utils.statement_parser.OpenAI")
@patch("api.utils.statement_parser.logger")
def test_extract_statement_details_success(mock_logger, mock_openai, mock_redact):
    """Tests successful extraction of statement details."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    transactions = [
        {
            "merchant": "Store",
            "date": "2024-01-01",
            "amount": 10.5,
            "currency": "USD",
            "transaction_type": "Expense",
        },
        {
            "merchant": "Cafe",
            "date": "2024-01-02",
            "amount": 5.0,
            "currency": "USD",
            "transaction_type": "Expense",
        },
    ]
    mock_redact.side_effect = lambda csv_text: f"REDACTED:{csv_text}"
    mock_message.function_call.arguments = json.dumps({"transactions": transactions})
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai.return_value = mock_client
    os.environ["OPENAI_API_KEY"] = "dummy"
    result = extract_statement_details(
        statement_text="statement text",
        prompt_set="card_account_csv_statement_parser",
    )
    assert result == transactions
    mock_logger.info.assert_any_call("Redacted PII from statement text.")
    mock_logger.info.assert_any_call("Received response from OpenAI API.")
    mock_logger.info.assert_any_call("Extracted %d transactions.", 2)


@patch("api.utils.statement_parser.logger")
def test_extract_statement_details_invalid_prompt_set(mock_logger):
    """Tests that an invalid prompt set raises a ValueError."""
    with pytest.raises(ValueError) as excinfo:
        extract_statement_details(
            statement_text="text", prompt_set="nonexistent_prompt"
        )
    assert "Prompt set 'nonexistent_prompt' not found in PROMPTS dictionary" in str(
        excinfo.value
    )
    mock_logger.error.assert_called_with("Invalid prompt set: %s", "nonexistent_prompt")


@patch("api.utils.statement_parser.logger")
def test_extract_statement_details_no_api_key(mock_logger):
    """Tests that missing OPENAI_API_KEY environment variable raises a ValueError."""
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
    with pytest.raises(ValueError) as excinfo:
        extract_statement_details(
            statement_text="statement text",
            prompt_set="card_account_csv_statement_parser",
        )
    assert "OPENAI_API_KEY environment variable is not set." in str(excinfo.value)
    mock_logger.error.assert_called_with(
        "OPENAI_API_KEY environment variable is not set."
    )


@patch("api.utils.statement_parser.remove_pii_columns")
@patch("api.utils.statement_parser.OpenAI")
@patch("api.utils.statement_parser.logger")
def test_extract_statement_details_invalid_json(mock_logger, mock_openai, mock_redact):
    """Tests that invalid JSON in the OpenAI response raises a ValueError."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_redact.side_effect = lambda csv_text: f"REDACTED:{csv_text}"
    mock_message.function_call.arguments = "not a json"
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai.return_value = mock_client
    os.environ["OPENAI_API_KEY"] = "dummy"
    with pytest.raises(ValueError) as excinfo:
        extract_statement_details(
            statement_text="statement text",
            prompt_set="card_account_csv_statement_parser",
        )
    assert "Failed to parse the response from OpenAI API." in str(excinfo.value)
    mock_logger.error.assert_any_call(
        "Parsing model response failed: %s", mock_logger.error.call_args[0][1]
    )


@patch("api.utils.statement_parser.remove_pii_columns")
@patch("api.utils.statement_parser.OpenAI")
def test_extract_statement_details_results_not_dict(mock_openai, mock_redact):
    """Tests that if `transactions` object is not a dict, a ValueError is raised."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_redact.side_effect = lambda csv_text: f"REDACTED:{csv_text}"
    mock_message.function_call.arguments = json.dumps(["not a dict"])
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai.return_value = mock_client
    os.environ["OPENAI_API_KEY"] = "dummy"
    with pytest.raises(ValueError) as excinfo:
        extract_statement_details(
            statement_text="statement text",
            prompt_set="card_account_csv_statement_parser",
        )
    assert "Expected response to be a dict" in str(excinfo.value)


@patch("api.utils.statement_parser.remove_pii_columns")
@patch("api.utils.statement_parser.OpenAI")
@patch("api.utils.statement_parser.logger")
def test_extract_statement_details_transaction_not_dict(
    mock_logger, mock_openai, mock_redact
):
    """Tests successful extraction of statement details."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    transactions = ["merchant"]
    mock_redact.side_effect = lambda csv_text: f"REDACTED:{csv_text}"
    mock_message.function_call.arguments = json.dumps({"transactions": transactions})
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai.return_value = mock_client
    os.environ["OPENAI_API_KEY"] = "dummy"
    with pytest.raises(ValueError) as excinfo:
        extract_statement_details(
            statement_text="statement text",
            prompt_set="card_account_csv_statement_parser",
        )
    assert "is not a dictionary" in str(excinfo.value)


@patch("api.utils.statement_parser.remove_pii_columns")
@patch("api.utils.statement_parser.OpenAI")
def test_extract_statement_details_transaction_missing_fields(mock_openai, mock_redact):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_redact.side_effect = lambda csv_text: f"REDACTED:{csv_text}"
    mock_message.function_call.arguments = json.dumps(
        {"transactions": [{"merchant": "A", "date": "2024-01-01", "amount": 1.0}]}
    )
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai.return_value = mock_client
    os.environ["OPENAI_API_KEY"] = "dummy"
    with pytest.raises(ValueError) as excinfo:
        extract_statement_details(
            statement_text="statement text",
            prompt_set="card_account_csv_statement_parser",
        )
    assert "is missing expected fields" in str(excinfo.value)
    assert "currency" in str(excinfo.value)


@patch("api.utils.statement_parser.remove_pii_columns")
@patch("api.utils.statement_parser.OpenAI")
@patch("api.utils.statement_parser.logger")
def test_extract_statement_details_openai_error(mock_logger, mock_openai, mock_redact):
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = OpenAIError("fail")
    mock_openai.return_value = mock_client
    mock_redact.side_effect = lambda csv_text: f"REDACTED:{csv_text}"
    os.environ["OPENAI_API_KEY"] = "dummy"
    with pytest.raises(RuntimeError) as excinfo:
        extract_statement_details(
            statement_text="statement text",
            prompt_set="card_account_csv_statement_parser",
        )
    assert "Failed to call OpenAI API." in str(excinfo.value)
    args_list = mock_logger.error.call_args_list
    assert any(
        call_args[0][0] == "OpenAI API call failed: %s"
        and str(call_args[0][1]) == "fail"
        for call_args in args_list
    )
