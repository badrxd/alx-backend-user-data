#!/usr/bin/env python3
'''authentication file'''
from api.v1.auth.auth import Auth
import base64


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
        except Exception:
            return None
        return key.decode('utf-8')

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        '''function that returns the user email and
        password from the Base64 decoded value'''
        if (not decoded_base64_authorization_header or
                type(decoded_base64_authorization_header) is not str):
            return (None, None)
        credentials = decoded_base64_authorization_header.split(":")

        if len(credentials) != 2:
            return (None, None)
        return tuple(credentials)
