#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session() -> str:
    """ POST /auth_session/login
    Return:
      - the user information width the coockies for the Session authentication
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    if not password or len(password) == 0:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    user = user.to_json()
    session_id = auth.create_session(user.get('id'))
    out = jsonify(user)
    out.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return out


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ DELETE /auth_session/logout
    Return:
      - delete the Session from cookies if the is one,
      Otherwise wase error 404 will be raised
    """
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200
