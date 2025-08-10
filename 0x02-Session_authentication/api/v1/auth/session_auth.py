#!/usr/bin/env python3
""" Session Authentication module"""
from api.v1.auth.auth import Auth
from flask import jsonify
from uuid import uuid4


class SessionAuth(Auth):
    """ SessionAuth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:  # type: ignore
        """ creates session ID for a user_id"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self,
                               session_id: str = None) -> str:  # type: ignore
        """ returns a User ID based on session ID"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        user_id = str(SessionAuth.user_id_by_session_id.get(session_id))
        return user_id

    def current_user(self, request=None):
        """ returns User instance based on a cookie value"""
        from models.user import User
        session_id = str(self.session_cookie(request))
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)

        return user

    def destroy_session(self, request=None):
        """deletes the user session/logout"""
        from models.user import User
        if request is None:
            return False
        if not self.session_cookie(request):
            return False
        session_id = str(self.session_cookie(request))
        if session_id:
            user_id = self.user_id_for_session_id(session_id)
            if not user_id:
                return False
            user = User.get(user_id)
            user_dict = jsonify(user.to_json())
            user_dict.set_cookie(session_id, '', expires=0)
            return True
