#!/usr/bin/env python3
""" Filtered logger"""
import logging
import os
import mysql.connector
import re
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract
from typing import List, Union


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

    logger.propagate = False

    return logger

def get_db() -> Union[MySQLConnection, PooledMySQLConnection, MySQLConnectionAbstract]:
    """returns a connector to a database"""
    connector = mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        user=os.getenv("PERSONAL_DATA_DB_USER", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )
    return connector


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
