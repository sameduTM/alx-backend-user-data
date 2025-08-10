#!/usr/bin/env python3
""" Basic auth - inherits from Auth"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """ BasicAuth class"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ returns the Base64 part of Auth header for Basic Auth
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split('Basic ')[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Returns decode value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decodedb64 = base64.b64decode(base64_authorization_header)
            return decodedb64.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """return use email and password from Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if not decoded_base64_authorization_header.__contains__(':'):
            return None, None
        email_pass = decoded_base64_authorization_header.split(':', 1)
        return email_pass[0], email_pass[1]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Return the User instance based on his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            user = User.search({"email": user_email})[0]
            assert user.is_valid_password(user_pwd) is True
            return user
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """ Overloads Auth and retrieves the User instance for a request"""
        auth_header = Auth.authorization_header(self, request)

        extract_64 = self.extract_base64_authorization_header(auth_header)

        decode_64 = self.decode_base64_authorization_header(extract_64)

        extract_user_cr = self.extract_user_credentials(decode_64)

        user_obj = self.user_object_from_credentials(extract_user_cr[0],
                                                     extract_user_cr[1])

        return user_obj
