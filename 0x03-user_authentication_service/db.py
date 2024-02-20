#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import Any
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

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add User
        """
        user = User()
        user.email = email
        user.hashed_password = hashed_password
        if self.__session is None:
            self._session
        self.__session.add(user)
        self.__session.commit()
        return user

    def find_user_by(self, **kwargs: Any) -> User:
        """Find user"""
        try:
            user = self.__session.query(User).filter_by(**kwargs).first()
            if not user:
                raise NoResultFound
            return user
        except InvalidRequestError as e:
            raise e

    def update_user(self, id: int, **kwargs: Any) -> None:
        """update use inforamtions"""
        try:
            user = self.find_user_by(id=id)
            for key, val in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, val)
                else:
                    raise ValueError
            self.__session.commit()
            return None
        except Exception as e:
            raise e
