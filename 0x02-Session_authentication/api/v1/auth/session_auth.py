#!/usr/bin/env python3
"""session authentication module"""
from typing import TypeVar
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """ SessionAuth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:  # type: ignore
        """creates a session ID for a user_id"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self,
                               session_id: str = None) -> str:  # type: ignore
        """returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        user_id = SessionAuth.user_id_by_session_id.get(session_id)
        return user_id  # type: ignore

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """returns User instance based on a cookie value"""
        from models.user import User

        session_id = str(self.session_cookie(request))
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """ deletes the user session / logout"""
        if request is None:
            return False
        if self.session_cookie(request) is None:
            return False
        session_id = str(self.session_cookie(request))
        if self.user_id_for_session_id(session_id) is None:
            return False
        del self.user_id_by_session_id[session_id]

        return True
