#!/usr/bin/env python3
"""handles all routes for the Session authentication"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
from os import getenv
from typing import Union


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Union[dict, tuple]:
    """session login"""
    from api.v1.app import auth

    user_email = request.form.get('email')
    user_pwd = request.form.get('password')

    if user_email is None:
        return jsonify({"error": "email missing"}), 400
    if user_pwd is None:
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": user_email})
    if not user:
        return jsonify({"error": "no user found this email"}), 404
    user = User.search({"email": user_email})[0]
    if not user.is_valid_password(user_pwd):
        return jsonify({"error": "wrong password"}), 401

    user_id = user.id

    session_id = auth.create_session(user_id)

    user_dict = jsonify(user.to_json())

    cookie_name = getenv("SESSION_NAME")

    user_dict.set_cookie(cookie_name, session_id)

    return user_dict


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """Logout"""
    from api.v1.app import auth
    destroy_session = auth.destroy_session(request)
    if not destroy_session:
        abort(404)
    return jsonify({}), 200
