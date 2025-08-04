#!/usr/bin/env python3
"""Regex-ing"""
import re


def filter_datum(fields, redaction, message, separator):
    """Returns log message with specified fields redacted."""
    pattern = f"({'|'.join(fields)})=.*?(?={separator}|$)"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
