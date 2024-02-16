#!/usr/bin/env python3
'''authentication file'''
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    '''SessionDBAuth class'''

    def create_session(self, user_id=None):
        '''create_session'''
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        sessionAuth = UserSession(
            **{'user_id': user_id, 'session_id': session_id})
        # sessionAuth.created_at = self.user_id_by_session_id.get(session_id)[
        #     'created_at']
        sessionAuth.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''user_id_for_session_id'''
        if not session_id:
            return None
        session_dictionary = UserSession.search({'session_id': session_id})
        # session_dictionary = UserSession().get(session_id)
        if not session_dictionary:
            return None
        session_dictionary = session_dictionary[0]
        user_id = session_dictionary.user_id
        if self.session_duration <= 0:
            return user_id
        created_at = session_dictionary.created_at
        if not created_at:
            return None
        session_Exp = (created_at) + timedelta(seconds=self.session_duration)
        if session_Exp < datetime.utcnow():
            return None
        return user_id

    def destroy_session(self, request=None):
        '''methode that destroy session if there is one'''
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        if not self.user_id_for_session_id(session_id):
            return False
        session_dictionary = UserSession.search({"session_id": session_id})
        if not session_dictionary:
            return False
        session_dictionary[0].remove()
        UserSession.save_to_file()
        return True
