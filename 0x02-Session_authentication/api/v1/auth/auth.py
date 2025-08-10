#!/usr/bin/env python3
""" manage API authentication"""
from typing import List, TypeVar
import os
import re


class Auth:
    """ Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ public method
            Return: False - path and excluded_paths
        """
        if path and not path.endswith('/'):
            path += '/'
        if not excluded_paths or excluded_paths is None:
            return True
        for ex_path in excluded_paths:
            if ex_path.__contains__('*'):
                ex_path = ex_path.replace('*', '.*')
            if re.match(ex_path, path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ public method
            Return: None
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """ public method
            Return: None
        """
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request is None:
            return None
        if os.getenv("SESSION_NAME") == "_my_session_id":
            cookie_value = request.cookies.get("_my_session_id")

            return cookie_value
