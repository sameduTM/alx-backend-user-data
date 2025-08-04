#!/usr/bin/env python3
"""Regex-ing"""
import re
import typing


def filter_datum(fields: typing.List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Returns log message with specified fields redacted."""
    pattern = f"({'|'.join(fields)})=.*?(?={separator}|$)"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
