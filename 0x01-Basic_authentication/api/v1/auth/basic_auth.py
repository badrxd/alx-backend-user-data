#!/usr/bin/env python3
'''authentication file'''
from api.v1.auth.auth import Auth
from models.base import Base
from models.user import User
import base64
from typing import TypeVar
from flask import request, abort


class BasicAuth(Auth):
    '''BasicAuth class'''

    def __init__(self) -> None:
        pass

    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        '''return the value after Basic : key'''
        if (not authorization_header or
                type(authorization_header) is not str
                or not authorization_header.startswith('Basic ')):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        '''function that returns the decoded value of a Base64 string'''
        if (not base64_authorization_header or
                type(base64_authorization_header) is not str):
            return None
        key = ''
        try:
            key = base64.b64decode(base64_authorization_header)
            return key.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        '''function that returns the user email and
        password from the Base64 decoded value'''
        if (not decoded_base64_authorization_header or
                type(decoded_base64_authorization_header) is not str):
            return (None, None)
        credentials = decoded_base64_authorization_header.split(":")

        if len(credentials) < 2:
            return (None, None)
        email = credentials[0]
        passwd = decoded_base64_authorization_header[len(email)+1:]
        return (email, passwd)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        '''function that returns the User instance
        based on his email and password.'''
        if (not user_email or not user_pwd or type(user_email) is not str
                or type(user_pwd) is not str):
            return None
        user = User().search({'email': user_email})
        if len(user) == 0:
            return None
        if user[0].is_valid_password(user_pwd) is False:
            return None
        return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        '''return user if he is authorized and authenticated
        otherwise rise http error 403
        '''
        token = self.extract_base64_authorization_header(
            request.headers.get('Authorization'))
        if token is None:
            return None
        valid_token = self.decode_base64_authorization_header(token)
        if valid_token is None:
            return None
        user_credentials = self.extract_user_credentials(valid_token)
        user = self.user_object_from_credentials(
            user_credentials[0], user_credentials[1])
        if user is None:
            return None

        return user
