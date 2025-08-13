#!/usr/bin/env python3
"""Hash password module"""
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from user import User
import bcrypt


def _hash_password(password: str) -> bytes:
    """takes in a password string arguments and returns bytes."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid(self) -> str:
    """return a string representation of a new UUID"""
    new_uuid = str(uuid4())
    return new_uuid


class Auth:
    """Auth class to interact with the authentication database"""

    def __init__(self) -> None:
        self._db = DB()

    def register_user(self, email: str,
                      password: str) -> User:  # type: ignore
        """register user"""
        hashed_pwd = _hash_password(password)
        try:
            user_check = self._db.find_user_by(email=email)
            if user_check:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            user = self._db.add_user(email, hashed_pwd.decode())
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """validate credentials"""
        try:
            user_check = self._db.find_user_by(email=email)
            if user_check:
                hashed_password = user_check.hashed_password
                if bcrypt.checkpw(password.encode(), hashed_password.encode()):
                    return True
            return False
        except Exception:
            return False
