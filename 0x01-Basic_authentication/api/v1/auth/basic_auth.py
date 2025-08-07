#!/usr/bin/env python3
""" Basic auth - inherits from Auth"""
from api.v1.auth.auth import Auth
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
        email_pass = decoded_base64_authorization_header.split(':')
        return email_pass[0], email_pass[1]
