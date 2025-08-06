#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt
from typing import ByteString


def hash_password(password: str) -> ByteString:
    """return a salted, hashed password - byte string"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
