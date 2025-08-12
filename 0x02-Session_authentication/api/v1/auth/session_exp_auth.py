#!/usr/bin/env python3
"""add expiration date to a Session ID"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class"""

    def __init__(self) -> None:
        """Instantiation method"""
        try:
            self.session_duration = int(
                os.getenv("SESSION_DURATION"))  # type: ignore
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:  # type: ignore
        """create session ID"""
        try:
            session_id = super().create_session(user_id)
            self.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
            }
            return session_id
        except Exception:
            return None  # type:  ignore

    def user_id_for_session_id(
            self, session_id: str = None) -> str:  # type:  ignore
        """Overload user_id_for_session_id"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None  # type:  ignore
        if isinstance(
                self.session_duration, int) and self.session_duration <= 0:
            return self.user_id_by_session_id[session_id]["user_id"]
        if "created_at" not in self.user_id_by_session_id[session_id]:
            return None  # type:  ignore
        created_at = self.user_id_by_session_id[session_id]["created_at"]
        if created_at + timedelta(
                seconds=self.session_duration) < datetime.now(  # type:  ignore
        ):
            return None  # type:  ignore
        return self.user_id_by_session_id[session_id]["user_id"]
