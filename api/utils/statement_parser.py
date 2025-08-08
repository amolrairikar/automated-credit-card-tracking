import json
import os
import logging

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from api.utils.prompts import PROMPTS
from api.utils.redact_pii import remove_pii_columns
from api.utils.setup_logger import setup_logger

load_dotenv()
logger = setup_logger(__name__, level=logging.INFO)


def extract_statement_details(
    statement_text: str, prompt_set: str
) -> dict[str, str | float]:
    """
    Extracts transaction or balance details from statement_text using OpenAI's gpt-4.1-mini model.
    The AI knows how to parse the statement based on the provided prompt set.

    Args:
        statement_text (str): The raw statement text from the input statement file containing transaction or balance
            details. This text is pre-processed to redact any PII such as account numbers, addresses, and names.
        prompt_set (str): The prompt set to provide the AI model with details on which data to extract
            from the statement text and the desired format.

    Returns:
        transaction_data (dict[str, str|float]): A dictionary containing extracted transaction details.
    """
    if prompt_set not in PROMPTS:
        logger.error("Invalid prompt set: %s", prompt_set)
        raise ValueError(f"Prompt set '{prompt_set}' not found in PROMPTS dictionary.")
    if os.environ.get("OPENAI_API_KEY") is None:
        logger.error("OPENAI_API_KEY environment variable is not set.")
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    try:
        statement_text = remove_pii_columns(csv_text=statement_text)
        logger.info("Redacted PII from statement text.")
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": PROMPTS[prompt_set]["system_prompt"]},
                {
                    "role": "user",
                    "content": PROMPTS[prompt_set]["user_prompt"].replace(
                        "REPLACE_ME", statement_text
                    ),
                },
            ],
            functions=[PROMPTS[prompt_set]["function_schema"]],
            function_call={"name": "extract_transaction"},
        )
        logger.info("Received response from OpenAI API.")
        function_args = response.choices[0].message.function_call.arguments
        all_transactions = json.loads(function_args)
        if not isinstance(all_transactions, dict):
            raise ValueError(
                f"Expected response to be a dict, got type {type(all_transactions)}."
            )
        transactions = all_transactions.get("transactions", [])
        for transaction in transactions:
            if not isinstance(transaction, dict):
                raise ValueError(f"Transaction {transaction} is not a dictionary.")
            expected_keys = {"merchant", "date", "amount", "currency"}
            missing = expected_keys - transaction.keys()
            if missing:
                raise ValueError(
                    f"Transaction {transaction} is missing expected fields: {missing}"
                )
        logger.info("Extracted %d transactions.", len(transactions))
        return transactions
    except (AttributeError, KeyError, json.JSONDecodeError) as e:
        logger.error("Parsing model response failed: %s", e)
        raise ValueError("Failed to parse the response from OpenAI API.")
    except OpenAIError as e:
        logger.error("OpenAI API call failed: %s", e)
        raise RuntimeError("Failed to call OpenAI API.")
