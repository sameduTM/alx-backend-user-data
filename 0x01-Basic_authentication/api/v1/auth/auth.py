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
        return False

    def authorization_header(self, request=None) -> str:
        """ public method
            Return: None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ public method
            Return: None
        """
        return None
