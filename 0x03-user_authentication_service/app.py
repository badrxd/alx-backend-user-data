#!/usr/bin/env python3
"""
Route module for the project
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def main_app():
    """main route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """ POST /users
    Job:
      - add user
    Return:
      - message
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ POST /sessions
    Job:
      - validate user login, and set session id as a coockies
    Return:
      - json
    """
    email = request.form.get('email')
    password = request.form.get('password')
    login_status = AUTH.valid_login(email, password)
    if login_status is False:
        abort(401)
    session_id = AUTH.create_session(email)
    out = jsonify({"email": f"<{email}", "message": "logged in"})
    out.set_cookie("session_id", session_id)
    return out


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ DELETE /sessions
    Job:
      - delete the session and redirect the user to the main page
    Return:
      - redirect
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ GET /profile
    Return:
      - json
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": f"{user.email}"}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ POST /reset_password
    Return:
      - json or raise HTTPException 403
    """
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """ PUT /reset_password
    Return:
      - json or raise HTTPException 403
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        user = AUTH._db.find_user_by(email=email)
        if user.reset_token != reset_token:
            abort(403)
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": f"{email}", "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
