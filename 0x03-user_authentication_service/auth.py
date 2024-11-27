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

    def create_session(self, email: str) -> str:
        """Creates a session
        Returns:
            The session id
        """
        try:
            u = self._db.find_user_by(email=email)
            session_id = str(uuid.uuid4())
            self._db.update_user(u.id, session_id=session_id)
            return session_id
        except NoResultFound:
            pass

    def get_user_by_session_id(self, session_id: str) -> user.User:
        """Returns a user acccount object by session id
        """
        if not session_id:
            return
        try:
            u = self._db.find_user_by(session_id=session_id)
            return u
        except NoResultFound:
            pass

    def destroy_session(self, user_id: str) -> None:
        """Destroys a user session
        """
        if not user_id:
            return
        try:
            u = self._db.find_user_by(id=user_id)
            setattr(u, "session_id", None)
            None
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Generates a token
        """
        if not email:
            print("User DNE")
            raise ValueError('User DNE')
        try:
            u = self._db.find_user_by(email=email)
        except NoResultFound:
            print("User DNE")
            raise ValueError('User DNE')
        token = str(uuid.uuid4())
        self._db.update_user(u.id, reset_token=token)
        return token
