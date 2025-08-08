import csv
import io

from api.utils.setup_logger import setup_logger

logger = setup_logger(__name__)


def remove_pii_columns(csv_text: str) -> str:
    """Removes PII columns from the given CSV text.

    Args:
        text (str): The input CSV text string containing PII columns.

    Returns:
        str: The CSV text with PII redacted.
    """
    if not csv_text:
        logger.error("Detected empty CSV file")
        raise ValueError("CSV text cannot be empty")
    cols_to_remove = [
        "Card No.",
        "Check or Slip #",
        "From",
        "To",
    ]
    lines = csv_text.splitlines()
    reader = csv.DictReader(lines)
    fieldnames = [f for f in reader.fieldnames if f not in cols_to_remove]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in reader:
        for col in cols_to_remove:
            if None in row:
                del row[None]
            row.pop(col, None)
        writer.writerow(row)

    return output.getvalue()
