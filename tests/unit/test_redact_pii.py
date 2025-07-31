from api.utils.redact_pii import redact_card_account_numbers


def test_redacts_single_card_number():
    """Tests that a single card account number is redacted correctly."""
    text = "Your card ending in 1234 was used."
    result = redact_card_account_numbers(text)
    assert result == "Your card ending in [REDACTED] was used."


def test_redacts_card_number_case_insensitive():
    """Tests that card account numbers are redacted regardless of the case
    of the preceding phrase."""
    text = "Payment from Card Ending in 5678 confirmed."
    result = redact_card_account_numbers(text)
    assert result == "Payment from Card Ending in [REDACTED] confirmed."


def test_redacts_multiple_card_numbers():
    """Tests that multiple card account numbers in the same text are redacted."""
    text = "Card ending in 1111 and card ending in 2222 are both active."
    result = redact_card_account_numbers(text)
    assert (
        result
        == "Card ending in [REDACTED] and card ending in [REDACTED] are both active."
    )


def test_no_card_number_pattern():
    """Tests that text without card account numbers remains unchanged."""
    text = "No card information here."
    result = redact_card_account_numbers(text)
    assert result == text


def test_does_not_redact_similar_but_invalid_pattern():
    """Tests that text with similar patterns that do not match the card account number format
    are not redacted."""
    text = "Card ending in 12345 is not valid."
    result = redact_card_account_numbers(text)
    assert result == text


def test_numbers_not_preceded_by_ending_in():
    """Tests that numbers not preceded by 'ending in' are not redacted."""
    text = "Card number 1234 is not redacted."
    result = redact_card_account_numbers(text)
    assert result == text
