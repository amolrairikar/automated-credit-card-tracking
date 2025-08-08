PROMPTS = {
    "card_account_csv_statement_parser": {
        "system_prompt": (
            "You are a helpful assistant that extracts structured transaction details from credit card CSV statements. "
            "You understand common financial data formats and accurately identify transactions within rows of tabular CSV content. "
        ),
        "user_prompt": (
            "Extract all valid transactions from the following CSV-formatted credit card statement. "
            "Return a JSON object with a 'transactions' key containing a list of all transactions. "
            "Each transaction must include the following fields: "
            "- 'merchant': the merchant or transaction description, "
            "- 'date': the transaction date in YYYY-MM-DD format, "
            "- 'amount': the transaction amount as a number (use negative values for refunds or credits), "
            "- 'currency': the currency code (e.g., USD). "
            "- 'transaction_type': the type of transaction, this should always be 'Expense'"
            "The CSV may or may not include a header row. If the first row appears to contain column names (e.g., contains labels like 'Date', 'Amount', or 'Description'), treat it as a header. "
            "If no header is detected, assume the columns follow a common credit card CSV layout and infer their meaning based on content patterns (e.g., dates, numbers, text descriptions). "
            "Exclude any rows that do not represent actual transactions, such as summaries or footers. "
            "If column names vary, use your best judgment to identify the merchant (e.g., 'Description', 'Merchant', 'Vendor' may all indicate the merchant). "
            "If the currency is not specified, assume 'USD'. Normalize all dates to YYYY-MM-DD format. "
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
                                "transaction_type": {
                                    "type": "string",
                                    "description": "The type of transaction, e.g., 'Expense'",
                                },
                            },
                            "required": [
                                "merchant",
                                "date",
                                "amount",
                                "currency",
                                "transaction_type",
                            ],
                        },
                    }
                },
                "required": ["transactions"],
            },
        },
    },
    "checking_account_csv_statement_parser": {
        "system_prompt": (
            "You are a helpful assistant that extracts structured transaction details from checking account CSV statements. "
            "You understand common financial data formats and accurately identify transactions within rows of tabular CSV content. "
        ),
        "user_prompt": (
            "Extract all valid transactions from the following CSV-formatted credit card statement. "
            "Return a JSON object with a 'transactions' key containing a list of all transactions. "
            "Each transaction must include the following fields: "
            "- 'merchant': the merchant or transaction description, "
            "- 'date': the transaction date in YYYY-MM-DD format, "
            "- 'amount': the transaction amount as a number (use absolute values), "
            "- 'currency': the currency code (e.g., USD). "
            "- 'transaction_type': the type of transaction, this should be 'Expense' for debits and 'Income' for credits."
            "The CSV may or may not include a header row. If the first row appears to contain column names (e.g., contains labels like 'Date', 'Amount', or 'Description'), treat it as a header. "
            "If no header is detected, assume the columns follow a common bank account CSV layout and infer their meaning based on content patterns (e.g., dates, numbers, text descriptions). "
            "Exclude any rows that do not represent actual transactions, such as summaries or footers. "
            "If column names vary, use your best judgment to identify the merchant (e.g., 'Description', 'Merchant', 'Vendor' may all indicate the merchant). "
            "If the currency is not specified, assume 'USD'. Normalize all dates to YYYY-MM-DD format. "
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
                                "transaction_type": {
                                    "type": "string",
                                    "description": "The type of transaction, e.g., 'Expense' or 'Income'",
                                },
                            },
                            "required": ["merchant", "date", "amount", "currency"],
                        },
                    }
                },
                "required": ["transactions"],
            },
        },
    },
}
