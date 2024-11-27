#!/usr/bin/env python3
"""DB module
"""
import user
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> user.User:
        """Creates a new user account
        """
        new = User(email=email, hashed_password=hashed_password)
        self._session.add(new)
        self._session.commit()
        return new

    def find_user_by(self, **kwargs) -> user.User:
        """Returns a user account object
        """
        try:
            obj = self._session.query(User).filter_by(**kwargs).first()
        except InvalidRequestError:
            raise InvalidRequestError
        if not obj:
            raise NoResultFound
        return obj

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updating a user account
        """
        attributes = ["id", "hashed_password", "email", "reset_token",
                      "session_id"]
        for k in kwargs:
            if k not in attributes:
                raise ValueError
        u = self.find_user_by(id=user_id)
        if u:
            for k, v in kwargs.items():
                u.__dict__[k] = v
            self._session.commit()
        return None
