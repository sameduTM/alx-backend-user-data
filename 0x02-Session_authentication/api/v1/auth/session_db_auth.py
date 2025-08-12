#!/usr/bin/env python3
"""authentication model"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from flask import abort
from datetime import datetime, timedelta
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """Session authentication class with DB"""

    def create_session(self, user_id=None) -> str:  # type: ignore
        """creates and stores new instance of UserSession and
           returns Session ID
        """
        from models.user_session import UserSession
        if user_id is None:
            return  # type: ignore
        session_id = super().create_session(user_id)
        user_session = UserSession()  # type: ignore

        user_session.user_id = user_id
        user_session.session_id = session_id
        user_session.save()

        return session_id

    def user_id_for_session_id(
            self, session_id: str = None) -> str:  # type: ignore
        """ returns the User ID by requesting UserSession in the database
            based on session_id
        """
        from models.user_session import UserSession
        if session_id is None:
            return None
        try:
            all_objects = [obj for obj in UserSession.all()]
        except KeyError:
            return None
        for obj in all_objects:
            if obj.session_id == session_id:
                # Check for expiration
                session_duration = getenv("SESSION_DURATION")
                if session_duration is not None:
                    try:
                        session_duration = int(session_duration)
                    except Exception:
                        session_duration = 0
                else:
                    session_duration = 0
                if session_duration <= 0:
                    return obj.user_id
                created_at = getattr(obj, "created_at", None)
                if created_at is None:
                    return None
                if isinstance(created_at, str):
                    created_at = datetime.fromisoformat(created_at)
                now = datetime.now()
                if created_at + timedelta(seconds=session_duration) < now:
                    obj.remove()  # Session expired, remove from DB
                    return None
                return obj.user_id
        return None

    def destroy_session(self, request=None) -> bool:
        """delete session"""
        from models.user_session import UserSession
        if request is None:
            return False
        session_id = request.cookies.get("_my_session_id")
        if not session_id:
            return False
        all_objects = [obj for obj in UserSession.all()]
        for obj in all_objects:
            if obj.to_json().get("session_id") == session_id:
                obj.remove()
                return True
        return False
