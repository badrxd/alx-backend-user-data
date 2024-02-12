#!/usr/bin/env python3
'''authentication file'''
from flask import request
from typing import List,  TypeVar


class Auth():
    '''class to manage the API authentication.'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''return False'''
        if (path is None or excluded_paths is None or
                excluded_paths == []):
            return True

        if path[-1] != "/":
            path = path+"/"

        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        '''return None'''
        if not request or not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        '''return None'''
        return None


class BasicAuth(Auth):
    '''BasicAuth class'''

    def __init__(self) -> None:
        pass
