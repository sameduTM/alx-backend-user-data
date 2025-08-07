#!/usr/bin/env python3
""" manage API authentication"""
from flask import request
from typing import List, TypeVar


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
        if path not in excluded_paths:
            return True
        if path in excluded_paths:
            return False

    def authorization_header(self, request=None) -> str:
        """ public method
            Return: None
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ public method
            Return: None
        """
        return None
