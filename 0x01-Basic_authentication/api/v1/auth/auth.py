#!/usr/bin/env python3
"""
Authentication module
"""
from flask import request as r
from typing import List, Optional


class Auth():
    """Authentication class"""
    def require_auth(self, path: str, execluded_paths: List[str]) -> bool:
        """Checks if "path" endpoint requires authentication
        """
        if not path:
            return True
        if not execluded_paths:
            return True
        if not path.endswith('/'):
            path += '/'
        if path in execluded_paths:
            return False
        else:
            for p in execluded_paths:
                if p.endswith("*"):
                    p = p[:-1]
                    if path.startswith(p):
                        return False
        return True

    def authorization_header(self, r=None) -> Optional[dict]:
        """To be fully implemented later"""
        if not r:
            return None
        auth_header = r.headers.get("Authorization")
        if not auth_header:
            return None
        return auth_header

    def current_user(self, r=None) -> None:
        """To be fully implemented later"""
        return None
