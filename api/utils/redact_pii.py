import re


def redact_card_account_numbers(text: str) -> str:
    """Redacts card account numbers from the given text.

    Args:
        text (str): The input text potentially containing card account numbers.

    Returns:
        str: The text with card account numbers redacted.
    """
    patterns = [r"(ending in )(\d{4})\b"]
    for pattern in patterns:
        text = re.sub(pattern, r"\1[REDACTED]", text, flags=re.IGNORECASE)
    return text
