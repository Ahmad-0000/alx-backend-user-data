#!/usr/bin/env python3
"""
Basic Authentication Module
"""
from api.v1.auth.auth import Auth
from os import getenv
import base64
from models.user import User


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

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extracts email and password
        """
        if not decoded_base64_authorization_header:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':')
        return email, password

    def user_object_from_credentials(self, user_email: str, user_pwd: str):
        """Searchs for a user account by email and password
        """
        if not user_email or not user_pwd:
            return None
        if type(user_email) is not str or type(user_pwd) is not str:
            return None
        matched_objects = User.search({"email": user_email})
        if not matched_objects:
            return None
        obj = matched_objects[0]
        if obj.valid_password(user_pwd):
            return obj
