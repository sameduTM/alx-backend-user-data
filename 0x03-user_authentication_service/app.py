#!/usr/bin/env python3
"""Basic flask app"""
from auth import Auth
from flask import Flask, jsonify, request, abort

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
    email, password = data.split('&')
    try:
        AUTH.register_user(email.split('=')[1], password.split('=')[1])
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
    AUTH.create_session(email)
    return jsonify({"email": email, "message": "logged in"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
