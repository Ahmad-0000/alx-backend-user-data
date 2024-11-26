#!/usr/bin/env python3
"""
Password encryption
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password
    """
    return bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())
