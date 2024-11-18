#!/usr/bin/env python3
"""
Basic Authentication Module
"""
from api.v1.auth.auth import Auth
from os import getenv
import base64


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes credentials encoded in base64
        """
        if not base64_authorization_header:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            return base64.b64decode(base64_authorization_header).\
                    decode('utf-8')
        except base64.binascii.Error:
            return None
