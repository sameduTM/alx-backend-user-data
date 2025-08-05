#!/usr/bin/env python3
""" Filtered logger"""
import logging
import re
from typing import List


PII_FIELDS = ('name', 'email', 'ssn', 'password', 'phone')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """returns the log message obfuscated"""
    pattern = r'(' + '|'.join(re.escape(field) + '='
                              for field in fields) + r')[^;]*'
    return re.sub(pattern, f"\\1{redaction}", message)


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    logger = logging.getLogger("user_data")

    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))

    logger.addHandler(console_handler)

    logger.propagate = True

    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)
