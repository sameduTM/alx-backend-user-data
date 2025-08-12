#!/usr/bin/env python3
"""UserSessession model that inherits from Base
    Store user sessions in DB
"""
from models.base import Base


class UserSession(Base):
    """User Session class"""
    user_id: str = None  # type: ignore
    session_id: str = None  # type: ignore

    def __init__(self, *args, **kwargs):
        """Initializes the class UserSession"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")  # type: ignore
        self.session_id = kwargs.get("session_id")  # type: ignore
