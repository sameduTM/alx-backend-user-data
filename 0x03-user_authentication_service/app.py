#!/usr/bin/env python3
"""Basic flask app"""
from auth import Auth
from flask import Flask, jsonify, request

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
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
