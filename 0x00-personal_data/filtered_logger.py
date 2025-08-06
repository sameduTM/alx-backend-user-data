#!/usr/bin/env python3
""" Filtered logger"""
import bcrypt
import logging
import os
import mysql.connector
import re
from mysql.connector import MySQLConnection
from typing import List, ByteString


PII_FIELDS = ('name', 'email', 'ssn', 'password', 'phone')


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


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """returns the log message obfuscated"""
    pattern = r'(' + '|'.join(re.escape(field) + '='
                              for field in fields) + fr')[^{separator}]*'
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


def get_db() -> MySQLConnection:
    """returns a connector to a database"""
    connector = mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        user=os.getenv("PERSONAL_DATA_DB_USER", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        database=os.getenv("PERSONAL_DATA_DB_NAME", "my_db")
    )
    return connector  # type: ignore


def main():
    """retrieve all rows in users tables and display each row under
        filtered format
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    # field names (column names)
    field_names = [i[0] for i in cursor.description]  # type: ignore
    rows = cursor.fetchall()
    message = ''
    for row in rows:
        for index, col in enumerate(row):
            message += f'{field_names[index]}={col};'
        message += '\n'
    message_list = message.split('\n')
    logger = get_logger()
    for msg in message_list[:-1]:
        logger.info(filter_datum(
            list(PII_FIELDS),
            RedactingFormatter.REDACTION,
            msg,
            RedactingFormatter.SEPARATOR))


if __name__ == "__main__":
    main()
