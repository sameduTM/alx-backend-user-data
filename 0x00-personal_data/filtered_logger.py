#!/usr/bin/env python3
"""Regex-ing"""
import re
import typing
import logging

def filter_datum(fields: typing.List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Returns log message with specified fields redacted."""
    pattern = f"({'|'.join(fields)})=.*?(?={separator}|$)"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: typing.List):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Log formatter"""
        original_message = super().format(record)
        redacted = filter_datum(
            self.fields, self.REDACTION, original_message, self.SEPARATOR)
        return redacted
