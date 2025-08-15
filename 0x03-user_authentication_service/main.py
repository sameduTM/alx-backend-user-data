#!/usr/bin/env python3
"""End-to-end integration test"""
from flask import abort, jsonify
import json
import requests


def register_user(email: str, password: str) -> None:
    """register user test case"""
    url = 'http://0.0.0.0:5000/users'
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(url, data=payload)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """log in with wrong password test case"""
    url = 'http://0.0.0.0:5000/sessions'
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(url, data=payload)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """log in successfully test case"""
    url = 'http://0.0.0.0:5000/sessions'
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(url, data=payload)
    assert response.json() == {"email": email, "message": "logged in"}
    assert response.status_code == 200
    for key in response.cookies.get_dict().keys():
        return key


def profile_unlogged() -> None:
    """not logged in profile route test case"""
    url = 'http://0.0.0.0:5000/profile'
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """profile logged in test case"""
    url = 'http://0.0.0.0:5000/profile'
    cookies = dict(session_id=session_id)
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """logout test case"""
    url = 'http://0.0.0.0:5000/sessions'
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """reset pwd token test case"""
    payload = {
        "email": email
    }
    response = requests.post('http://0.0.0.0:5000/reset_password',
                             data=payload)

    assert response.status_code == 200
    return response.json()["reset-token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update password test case"""
    url = 'http://0.0.0.0:5000/update_password'
    payload = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(url, data=payload)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
