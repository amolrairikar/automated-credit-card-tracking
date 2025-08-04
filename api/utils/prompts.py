PROMPTS = {
    "pdf_card_and_checking_statement_parser": {
        "system_prompt": (
            "You are a helpful assistant that extracts transaction details from credit card statements."
        ),
        "user_prompt": (
            "Extract all transactions from the following credit card statement, including purchases, "
            "refunds, fees, interest charges,and statement credits. "
            "Return a JSON object with a 'transactions' key that is a list of all transactions. "
            "Each transaction should have the following fields: "
            "- 'merchant': the name of the merchant or description of the transaction, "
            "- 'date': the date of the transaction in YYYY-MM-DD format, "
            "- 'amount': the amount of the transaction (use a negative value for refunds and credits), "
            "- 'currency': the currency used (e.g., USD), "
            "REPLACE_ME"
        ),
        "function_schema": {
            "name": "extract_transaction",
            "description": "Extracts structured transaction details from a credit card statement",
            "parameters": {
                "type": "object",
                "properties": {
                    "transactions": {
                        "type": "array",
                        "description": "List of transactions extracted from the statement",
                        "items": {
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
                                "amount": {
                                    "type": "number",
                                    "description": "The transaction amount",
                                },
                                "currency": {
                                    "type": "string",
                                    "description": "Currency used, e.g., USD",
                                },
                            },
                            "required": ["merchant", "date", "amount", "currency"],
                        },
                    }
                },
                "required": ["transactions"],
            },
        },
    }
}
