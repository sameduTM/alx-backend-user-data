#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS)


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if getenv("AUTH_TYPE"):
    if getenv("AUTH_TYPE") == "auth":
        from api.v1.auth.auth import Auth
        auth = Auth()
    if getenv("AUTH_TYPE") == "basic_auth":
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    if getenv("AUTH_TYPE") == "session_auth":
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()


@app.before_request
def filter_request():
    """ filter each request"""
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                      '/api/v1/forbidden/', '/api/v1/auth_session/login/']
    from api.v1.auth.session_auth import SessionAuth
    if auth is None:
        return
    request.current_user = auth.current_user(request)
    if not auth.require_auth(request.path, excluded_paths):  # type: ignore
        return
    session_id = SessionAuth.user_id_by_session_id
    print(session_id)
    if auth.session_cookie(request) is \
            None and auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404  # type: ignore


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401  # type: ignore


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden resource handler
    """
    return jsonify({"error": "Forbidden"}), 403  # type: ignore


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", 5000)
    app.debug = True
    app.run(host=host, port=port)
