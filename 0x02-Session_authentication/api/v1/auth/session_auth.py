#!/usr/bin/env python3
'''file : session for authenticated user'''
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    '''SessionAuth class'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''methode that creates a Session ID for a user_id'''
        if not user_id or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id.update({session_id: user_id})
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''methode that returns a User ID based on a Session ID'''
        if not session_id or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''methode that returns a User instance based on a cookie value'''
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User().get(user_id)
        return user
