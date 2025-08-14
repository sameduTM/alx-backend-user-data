#!/usr/bin/env python3
"""Basic flask app"""
from auth import Auth
from flask import Flask, jsonify, request, abort, make_response, redirect

app = Flask(__name__)

AUTH = Auth()


@app.route('/', methods=["GET"], strict_slashes=False)
def index():
    """default route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"], strict_slashes=False)
def register_user():
    """Register user"""
    email = str(request.form.get('email'))
    password = str(request.form.get('password'))
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login():
    """function to respond to the POST /sessions route."""
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(str(email), str(password)):
        abort(401)
    session_id = AUTH.create_session(str(email))
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie(session_id)

    return response


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout():
    """Log out"""
    session_id = str(request.cookies.get("session_id"))
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect('/', code=302)
    abort(403)


@app.route('/profile', methods=["GET"], strict_slashes=False)
def profile():
    """function to respond to the GET /profile route"""
    session_id = str(request.cookies.get('session_id'))
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
    abort(403)


@app.route('/reset_password', methods=["POST"], strict_slashes=False)
def reset_password():
    """reset password"""
    email = str(request.form.get('email'))
    try:
        reset_token = AUTH.get_reset_password_token(email)
        if reset_token:
            return jsonify({"email": email, "reset-token": reset_token})
        abort(403)
    except Exception:
        abort(403)


@app.route('/reset_password', methods=["PUT"], strict_slashes=False)
def update_password():
    """update password"""
    email = str(request.form.get('email'))
    reset_token = str(request.form.get('reset_token'))
    new_password = str(request.form.get('new_password'))
    try:
        if AUTH.update_password(reset_token, new_password) is None:
            return jsonify({"email": email, "message": "Password updated"})
        abort(403)
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
