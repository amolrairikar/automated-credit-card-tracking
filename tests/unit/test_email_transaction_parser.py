import json
import pytest
from unittest.mock import patch, MagicMock

from openai import OpenAIError

from api.email_transaction_parser import extract_email_transaction_details


def generate_openai_response(arguments_json):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.function_call.arguments = arguments_json
    return mock_response


@patch("api.email_transaction_parser.client")
def test_extract_transaction_details_success(mock_client):
    """Tests happy path for extract_transaction_details where transaction info is successfully extracted."""
    email_text = (
        "You spent $12.34 at Starbucks on 2024-06-01 using Chase Credit Card 5678."
    )
    transaction_dict = {
        "merchant": "Starbucks",
        "date": "2024-06-01",
        "amount": 12.34,
        "currency": "USD",
        "account": "Chase Credit Card 5678",
    }
    arguments_json = json.dumps(transaction_dict)
    mock_client.chat.completions.create.return_value = generate_openai_response(
        arguments_json
    )
    result = extract_email_transaction_details(email_text=email_text)
    assert result == transaction_dict


@patch("api.email_transaction_parser.client")
def test_extract_transaction_details_missing_fields(mock_client):
    email_text = "Missing fields."
    transaction_dict = {"merchant": "Starbucks", "date": "2024-06-01", "amount": 12.34}
    arguments_json = json.dumps(transaction_dict)
    mock_client.chat.completions.create.return_value = generate_openai_response(
        arguments_json
    )
    with pytest.raises(ValueError) as excinfo:
        extract_email_transaction_details(email_text=email_text)
    assert "Missing expected fields in response" in str(excinfo.value)


@patch("api.email_transaction_parser.logger")
@patch("api.email_transaction_parser.client")
def test_extract_transaction_details_malformed_json(mock_client, mock_logger):
    """Tests that extract_transaction_details raises ValueError when the OpenAI response is malformed."""
    email_text = "Malformed JSON"
    arguments_json = "{merchant: Starbucks,}"
    mock_client.chat.completions.create.return_value = generate_openai_response(
        arguments_json
    )
    with pytest.raises(ValueError) as excinfo:
        extract_email_transaction_details(email_text=email_text)
    assert "Failed to parse the response from OpenAI API." in str(excinfo.value)
    mock_logger.error.assert_called()


@patch("api.email_transaction_parser.logger")
@patch("api.email_transaction_parser.client")
def test_extract_transaction_details_attribute_error(mock_client, mock_logger):
    """Tests that extract_transaction_details raises ValueError when the OpenAI response is
    missing the `choices` attribute."""
    email_text = "Attribute error"
    mock_response = MagicMock()
    del mock_response.choices
    mock_client.chat.completions.create.return_value = mock_response
    with pytest.raises(ValueError) as excinfo:
        extract_email_transaction_details(email_text=email_text)
    assert "Failed to parse the response from OpenAI API." in str(excinfo.value)
    mock_logger.error.assert_called()


@patch("api.email_transaction_parser.logger")
@patch("api.email_transaction_parser.client")
def test_extract_transaction_details_openai_error(mock_client, mock_logger):
    email_text = "OpenAI error"
    mock_client.chat.completions.create.side_effect = OpenAIError("API error")
    with pytest.raises(RuntimeError) as excinfo:
        extract_email_transaction_details(email_text)
    assert "Failed to call OpenAI API." in str(excinfo.value)
    mock_logger.error.assert_called()
