#!/usr/bin/env python3
""""""
from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """crypting the user password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """methode return a string representation of a new UUID"""
    new_uuid = uuid4()
    return str(new_uuid)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register new user"""
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass
        password = _hash_password(password)
        user = self._db.add_user(email, password)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """validating the loginf info"""
        user = None
        if not email or not password:
            return False

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        if bcrypt.checkpw(password.encode(), user.hashed_password):
            return True
        else:
            return False

    def create_session(self, email: str) -> str:
        """
        methode that create new session id and save it in the user data
        Return:
          - session id or None if ther is no user
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """return user by session_id else return None"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """methode that destroy the session"""
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            pass
        return None

    def get_reset_password_token(self, email: str) -> str:
        """method take an email string argument and returns a string.
        token (uuid)
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """methode that update the password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            password = _hash_password(password)
            self._db.update_user(
                user.id, **{'hashed_password': password, 'reset_token': None})
        except NoResultFound:
            raise ValueError
        return None
