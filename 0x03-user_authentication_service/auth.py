#!/usr/bin/env python3
"""
Hashing passwords
"""
import bcrypt
import user
import uuid
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashing a password
    """
    return bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generating a uuid
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> user.User:
        """Registers a user account
        """
        try:
            u = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            u = self._db.add_user(email, hashed_password.decode("utf-8"))
            return u

    def valid_login(self, email: str, password: str) -> bool:
        """Validating credentials
        """
        try:
            u = self._db.find_user_by(email=email)
            if bcrypt.checkpw(bytes(password, "utf-8"),
                              bytes(u.hashed_password, "utf-8")):
                return True
            return False
        except NoResultFound:
            return False
