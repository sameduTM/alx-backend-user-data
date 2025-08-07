#!/usr/bin/env python3
""" Basic auth - inherits from Auth"""
from api.v1.auth.auth import Auth


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
