#!/usr/bin/env python3
'''authentication file'''
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    '''BasicAuth class'''

    def __init__(self) -> None:
        pass

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        '''return the value after Basic : key'''
        if (not authorization_header or
                type(authorization_header) is not str
                or not authorization_header.startswith('Basic ')):
            return None
        return authorization_header.split(" ")[1]
