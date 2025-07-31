import os
import json
import logging
from typing import Dict, Union

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from api.utils.setup_logger import setup_logger
from api.utils.redact_pii import redact_card_account_numbers

load_dotenv()
logger = setup_logger(logger_name="automated_credit_card_tracking", level=logging.INFO)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

system_prompt = (
    "You are a helpful assistant that extracts transaction details from emails."
)

function_schema = {
    "name": "extract_transaction",
    "description": "Extracts structured transaction details from an email",
    "parameters": {
        "type": "object",
        "properties": {
            "merchant": {
                "type": "string",
                "description": "The merchant or vendor name",
            },
            "date": {
                "type": "string",
                "description": "The date of transaction in YYYY-MM-DD format",
            },
            "amount": {"type": "number", "description": "The transaction amount"},
            "currency": {"type": "string", "description": "Currency used, e.g., USD"},
        },
        "required": ["merchant", "date", "amount", "currency"],
    },
}


def extract_email_transaction_details(email_text: str) -> Dict[str, Union[str, float]]:
    """Extracts transaction details from email_text using OpenAI's GPT model.

    Args:
        email_text (str): The raw email content containing transaction details.

    Returns:
        transaction_data (Dict[str, Union[str, float]]): A dictionary containing extracted transaction details.
    """
    try:
        email_text = redact_card_account_numbers(text=email_text)
        logger.info("Redacted card account numbers from email text.")
        user_prompt = (
            f"Extract the transaction details from the following email:\n\n{email_text}"
        )
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            functions=[function_schema],
            function_call={"name": "extract_transaction"},
        )
        logger.info("Received response from OpenAI API.")
        function_args = response.choices[0].message.function_call.arguments
        transaction_data = json.loads(function_args)
        expected_keys = {"merchant", "date", "amount", "currency"}
        missing = expected_keys - transaction_data.keys()
        if missing:
            raise ValueError(f"Missing expected fields in response: {missing}")
        return transaction_data
    except (AttributeError, KeyError, json.JSONDecodeError) as e:
        logger.error("Parsing model response failed: %s", e)
        raise ValueError("Failed to parse the response from OpenAI API.")
    except OpenAIError as e:
        logger.error("OpenAI API call failed: %s", e)
        raise RuntimeError("Failed to call OpenAI API.")
