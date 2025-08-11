#!/usr/bin/env python3
"""handles all routes for the Session authentication"""
from api.v1.views import app_views
from flask import request, jsonify
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def session_login():
    """session login"""
    from api.v1.app import auth
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not User.is_valid_password(user[0], password):
        return jsonify({"error": "wrong password"}), 401
    session_id = auth.create_session(user[0].id)
    user_object = jsonify(user[0].to_json())
    cookie_name = str(getenv("SESSION_NAME"))
    user_object.set_cookie(cookie_name, session_id)

    return user_object
