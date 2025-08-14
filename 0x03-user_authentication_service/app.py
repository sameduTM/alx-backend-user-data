#!/usr/bin/env python3
"""Basic flask app"""
from auth import Auth
from flask import Flask, jsonify, request, abort, make_response

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def index():
    """default route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """Register user"""
    data = request.get_data().decode('utf-8')
    credentials = data.split('&')
    email = credentials[0].split('=')[1]
    password = credentials[1].split('=')[1]
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """function to respond to the POST /sessions route."""
    data = request.get_data().decode()
    credentials = data.split('&')
    email = credentials[0].split('=')[1]
    password = credentials[1].split('=')[1]
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie(session_id)

    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
