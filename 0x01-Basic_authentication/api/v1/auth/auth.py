#!/usr/bin/env python3
'''authentication file'''
from flask import request
from typing import List,  TypeVar
import fnmatch


class Auth():
    '''class to manage the API authentication.'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''return False'''
        if (path is None or excluded_paths is None or
                excluded_paths == []):
            return True

        if path[-1] != "/":
            path = path+"/"

        for pattern in excluded_paths:
            if fnmatch.fnmatch(path, pattern):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        '''return None'''
        if not request or not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        '''return None'''
        return None
