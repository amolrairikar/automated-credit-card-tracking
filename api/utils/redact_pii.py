import os
import re
from typing import Pattern


def redact_pii(text: str) -> str:
    """Redacts PII from the given text.

    Args:
        text (str): The input text potentially containing PII.

    Returns:
        str: The text with PII redacted.
    """
    names = os.getenv("REDACT_NAMES", "").replace('"', "")
    name_list = [name.strip() for name in names.split(",") if name.strip()]
    patterns: dict[str, list[Pattern]] = {
        "account_numbers": [
            re.compile(r"(Account Ending\s+\d-\s*)(?P<pii>\d{5})\b", re.IGNORECASE),
            re.compile(r"(ending in\s+)(?P<pii>\d{4})\b", re.IGNORECASE),
            re.compile(r"(?P<pii>\b\d{15}\b)"),
            re.compile(r"(?P<pii>\b\d{16}\b)"),
            re.compile(r"(?P<pii>\b(?:\d{4}\s){3}\d{4}\b)"),
            re.compile(r"(?P<pii>\b\d{41}\b)"),
            re.compile(r"(?P<pii>\b\d{41})"),
            re.compile(r"(?P<pii>\b[a-zA-Z0-9]{26}\b)"),
            re.compile(r"(XXXX\sXXXX\sXXXX\s)(?P<pii>\d{4})\b"),
            re.compile(r"(Account Number Ending in\s+)(?P<pii>\d{4})\b", re.IGNORECASE),
            re.compile(r"(#)(?P<pii>\d{4})\b"),
        ],
        "addresses": [
            re.compile(
                r"(?P<pii>\b\d{1,6}\s+[\w\s]{2,30}?\s(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Way|Circle|Cir|Trail|Trl|Parkway|Pkwy|Place|Pl)\b\.?,?)",
                re.IGNORECASE,
            )
        ],
        "zip_codes": [re.compile(r"(?P<pii>\b\d{5}(?:-\d{4})?)\b")],
        "name": [re.compile(rf"(?P<pii>\b(?:{'|'.join(name_list)})\b)", re.IGNORECASE)],
    }
    for pattern_list in patterns.values():
        for pattern in pattern_list:
            text = pattern.sub(
                lambda m: m.group(0).replace(m.group("pii"), "[REDACTED]"), text
            )
    return text
