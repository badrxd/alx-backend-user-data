#!/usr/bin/env python3
'''Encrypting passwords'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''return hashed password'''
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed
