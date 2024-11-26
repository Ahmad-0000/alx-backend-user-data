#!/usr/bin/env python3
"""
Password encryption
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password
    """
    return bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if "hashed_password" is "password"
    """
    return bcrypt.checkpw(bytes(password, "utf-8"), hashed_password)
