#!/usr/bin/env python3
"""
Authentication module
"""
from flask import request as r
from typing import List


class Auth():
    """Authentication class"""
    def require_auth(self, path: str, execlueded_paths: List[str]) -> bool:
        """To be fully implemented later
        """
        return False

    def authorization_header(self, r=None) -> None:
        """To be fully implemented later"""
        return None

    def current_user(self, r=None) -> None:
        """To be fully implemented later"""
        return None
