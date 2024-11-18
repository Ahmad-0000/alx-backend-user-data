#!/usr/bin/env python3
"""
Basic Authentication Module
"""
from api.v1.auth.auth import Auth
from os import getenv


class BasicAuth(Auth):
    """Basic Authentication Mechanism Class"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts the base64-encoded username:password"""
        if not authorization_header:
            return
        if type(authorization_header) is not str:
            return
        if not authorization_header.startswith("Basic "):
            return
        try:
            return authorization_header.split()[1]
        except IndexError:
            return None
