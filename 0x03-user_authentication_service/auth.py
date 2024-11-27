#!/usr/bin/env python3
"""
Hashing passwords
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashing a password
    """
    return bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())
