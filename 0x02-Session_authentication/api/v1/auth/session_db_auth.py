#!/usr/bin/env python3
"""authentication model"""
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Session authentication class with DB"""

    def create_session(self, user_id=None) -> str:  # type: ignore
        """creates and stores new instance of UserSession and
           returns Session ID
        """
        from models.user_session import UserSession

        session_id = super().create_session(user_id)
        user_session = UserSession()  # type: ignore

        user_session.user_id = user_id
        user_session.session_id = session_id
        # user_session.id = session_id
        user_session.save()

        return session_id

    def user_id_for_session_id(
            self, session_id: str = None) -> str:  # type: ignore
        """ returns the User ID by requesting UserSession in the database
            based on session_id
        """
        from models.user_session import UserSession
        UserSession.load_from_file()
        all_objects = [obj.to_json() for obj in UserSession.all()]
        if session_id:
            for obj in all_objects:
                if obj["session_id"] == session_id:
                    return obj["user_id"]

    def destroy_session(self, request=None) -> bool:  # type: ignore
        """that destroys the UserSession based on the Session ID from the
           request cookie
        """
        from models.user_session import UserSession
        UserSession.load_from_file()
        all_objects = [obj for obj in UserSession.all()]
        if request:
            session_id = request.cookies.get("_my_session_id")
            for obj in all_objects:
                if obj.to_json()["session_id"] == session_id:
                    obj.remove()
