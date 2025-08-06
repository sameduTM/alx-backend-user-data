#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """return a salted, hashed password - byte string"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
