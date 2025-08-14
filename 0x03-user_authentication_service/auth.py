#!/usr/bin/env python3
"""Hash password module"""
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from user import User
import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """takes in a password string arguments and returns bytes."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database"""

    def __init__(self) -> None:
        """Initializes the Auth class"""
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

    def create_session(self, email: str) -> str:  # type: ignore
        """takes an email string argument and returns the session ID as
           a string.
        """
        try:
            find_user = self._db.find_user_by(email=email)
            if find_user:
                session_id = _generate_uuid()
                self._db.update_user(find_user.id, session_id=session_id)
                return session_id
        except Exception:
            return None  # type: ignore

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """takes a single session_id string argument and returns the
           corresponding User or None.
        """
        if session_id is None:
            return None
        try:
            find_user = self._db.find_user_by(session_id=session_id)
            return find_user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy session"""
        session_id = None
        self._db.update_user(user_id, session_id=session_id)
