#!/usr/bin/env python3
""""""
import bcrypt


def _hash_password(password: str) -> bytes:
    """crypting the user password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
