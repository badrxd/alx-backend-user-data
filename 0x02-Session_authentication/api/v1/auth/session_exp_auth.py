#!/usr/bin/env python3
'''file : Expiration session for authenticated user'''
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth (SessionAuth):
    '''SessionExpAuth class'''

    def __init__(self):
        ''''''
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        '''methode that creates a Expired Session for
        a user_id and return the session id'''
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''methode that returns a User ID based on a Session ID'''
        if not session_id:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if not session_dictionary:
            return None
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')
        created_at = session_dictionary.get('created_at')
        if not created_at:
            return None
        session_Exp = (created_at) + timedelta(seconds=self.session_duration)
        if session_Exp < datetime.now():
            return None
        return session_dictionary.get('user_id')
