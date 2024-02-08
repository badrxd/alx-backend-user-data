#!/usr/bin/env python3
'''Encrypting passwords'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''return hashed password'''
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """function that validate that the
    provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed_password)
