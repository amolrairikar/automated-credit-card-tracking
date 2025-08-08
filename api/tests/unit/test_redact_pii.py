import pytest

from api.utils.redact_pii import remove_pii_columns


def test_remove_pii_columns_removes_specified_columns():
    """Tests that columns matching removal criteria are removed."""
    csv_text = (
        "Card No.,Check or Slip #,From,To,Amount,Description\n"
        "1234,5678,Alice,Bob,100,Payment\n"
        "2345,6789,Carol,Dave,200,Refund\n"
    )
    expected_result = "Amount,Description\n100,Payment\n200,Refund\n"
    result = remove_pii_columns(csv_text)
    assert result == expected_result


def test_remove_pii_columns_if_no_pii_columns():
    """Tests that if no PII columns are present, the original text is returned."""
    csv_text = "Amount,Description\n100,Payment\n200,Refund\n"
    result = remove_pii_columns(csv_text)
    assert result == csv_text


def test_remove_pii_columns_raises_on_empty_input():
    """Tests that empty input CSV files raise a ValueError."""
    csv_text = ""
    with pytest.raises(ValueError) as excinfo:
        remove_pii_columns(csv_text)
    assert "CSV text cannot be empty" in str(excinfo.value)


def test_remove_pii_columns_handles_only_header():
    """Tests that if only columns are present, PII column headers are removed."""
    csv_text = "Card No.,Amount,Description\n"
    result = remove_pii_columns(csv_text)
    assert "Card No." not in result
    assert "Amount" in result
    assert "Description" in result


def test_remove_pii_columns_handles_none_column_key():
    """Tests that values from 'None' columns are removed"""
    csv_text = "Amount\n100,unexpected\n"
    expected_result = "Amount\n100\n"
    result = remove_pii_columns(csv_text)
    assert result == expected_result
