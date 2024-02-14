#!/usr/bin/env python3
'''file : session for authenticated user'''
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    '''SessionAuth class'''

    def __init__(self) -> None:
        self.user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''methode that creates a Session ID for a user_id'''
        if not user_id or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id.update({session_id: user_id})
        return session_id
