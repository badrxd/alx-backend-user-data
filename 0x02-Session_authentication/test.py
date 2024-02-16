#!/usr/bin/env python3
""" Main 4
"""
from flask import Flask, request
from api.v1.auth.session_db_auth import SessionDBAuth
from models.user import User


b = SessionDBAuth()
sess = b.create_session('666666666666666666666')
print(sess)

user = b.user_id_for_session_id(sess)
print(user)
