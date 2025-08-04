from api.utils.redact_pii import redact_pii


def test_redacts_single_card_number():
    """Tests that a single card account number is redacted correctly."""
    text = "Your card ending in 1234 was used."
    result = redact_pii(text)
    assert result == "Your card ending in [REDACTED] was used."


def test_redacts_card_number_case_insensitive():
    """Tests that card account numbers are redacted regardless of the case
    of the preceding phrase."""
    text = "Payment from Card Ending in 5678 confirmed."
    result = redact_pii(text)
    assert result == "Payment from Card Ending in [REDACTED] confirmed."


def test_redacts_multiple_card_numbers():
    """Tests that multiple card account numbers in the same text are redacted."""
    text = "Card ending in 1111 and card ending in 2222 are both active."
    result = redact_pii(text)
    assert (
        result
        == "Card ending in [REDACTED] and card ending in [REDACTED] are both active."
    )


def test_no_pii():
    """Tests that text without PII remains unchanged."""
    text = "No sensitive information here."
    result = redact_pii(text)
    assert result == text


def test_redacts_five_digit_numbers():
    """Tests that 5 digit card numbers are redacted."""
    text = "Card ending in 12345 was used."
    result = redact_pii(text)
    assert result == "Card ending in [REDACTED] was used."


def test_numbers_not_preceded_by_ending_in():
    """Tests that numbers not preceded by 'ending in' are not redacted."""
    text = "Card number 1234 is not redacted."
    result = redact_pii(text)
    assert result == text


def test_redacts_account_number_with_account_ending_pattern():
    text = "Account Ending 1- 54321 was used."
    result = redact_pii(text)
    assert result == "Account Ending 1- [REDACTED] was used."


def test_redacts_15_digit_number():
    text = "Sensitive number: 123456789012345"
    result = redact_pii(text)
    assert result == "Sensitive number: [REDACTED]"


def test_redacts_16_digit_number():
    text = "Sensitive number: 1234567890123456"
    result = redact_pii(text)
    assert result == "Sensitive number: [REDACTED]"


def test_redacts_16_digit_spaced_number():
    text = "Sensitive number: 1234 5678 9012 3456"
    result = redact_pii(text)
    assert result == "Sensitive number: [REDACTED]"


def test_redacts_41_digit_number():
    text = "Long number: 12345678901234567890123456789012345678901"
    result = redact_pii(text)
    assert result == "Long number: [REDACTED]"


def test_redacts_26_alphanumeric():
    text = "Alphanumeric: ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = redact_pii(text)
    assert result == "Alphanumeric: [REDACTED]"


def test_redacts_xxxx_pattern():
    text = "Card: XXXX XXXX XXXX 4321"
    result = redact_pii(text)
    assert result == "Card: XXXX XXXX XXXX [REDACTED]"


def test_redacts_hash_pattern():
    text = "Reference #1234"
    result = redact_pii(text)
    assert result == "Reference #[REDACTED]"


def test_redacts_address():
    text = "Send mail to 123 Main Street."
    result = redact_pii(text)
    assert result == "Send mail to [REDACTED]"


def test_redacts_zip_code():
    text = "My ZIP is 90210."
    result = redact_pii(text)
    assert result == "My ZIP is [REDACTED]."


def test_redacts_zip_plus4():
    text = "ZIP+4: 90210-1234"
    result = redact_pii(text)
    assert result == "ZIP+4: [REDACTED]"


def test_redacts_names_from_env(monkeypatch):
    monkeypatch.setenv("REDACT_NAMES", "Alice,Bob")
    text = "Alice and Bob went to the store."
    result = redact_pii(text)
    assert result == "[REDACTED] and [REDACTED] went to the store."


def test_redacts_name_from_env(monkeypatch):
    monkeypatch.setenv("REDACT_NAMES", "Charlie")
    text = "charlie paid."
    result = redact_pii(text)
    assert result == "[REDACTED] paid."


def test_redacts_multiple_patterns():
    text = "Card ending in 1234, ZIP 12345, and 456 Main St."
    result = redact_pii(text)
    assert result == "Card ending in [REDACTED], ZIP [REDACTED], and [REDACTED]"


def test_redacts_address_with_abbreviation():
    text = "Meet at 789 Elm Rd."
    result = redact_pii(text)
    assert result == "Meet at [REDACTED]"


def test_redacts_address_with_comma():
    text = "Send to 456 Oak Avenue, please."
    result = redact_pii(text)
    assert result == "Send to [REDACTED] please."


def test_empty_string():
    text = ""
    result = redact_pii(text)
    assert result == ""
