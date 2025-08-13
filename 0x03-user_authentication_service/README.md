# 🔐 User Authentication Service

A hands-on learning project to build a **secure user authentication system** using **Flask**, **SQLAlchemy**, and **bcrypt**.

> ⚠ **Note:** This project is for learning purposes only.  
> In production, always use established authentication frameworks like **Flask-Login** or **Django Auth**.

---

## ✨ Features

- **User registration** and **login**
- **Password hashing** with bcrypt
- **Session management** (cookie-based)
- **Password reset** via secure token
- **User profile** endpoint

---

## 🎯 Learning Objectives

By completing this project, you will learn:

- How to **declare API routes** in Flask
- How to **set and read cookies**
- How to **retrieve form data** from requests
- How to **return HTTP status codes**
- How to **interact with SQLAlchemy ORM**
- How to **securely store passwords** with bcrypt

---

## 📋 Requirements

**Environment:**
- Ubuntu 18.04 LTS
- Python 3.7
- SQLAlchemy **1.3.x**
- `pycodestyle` **2.5** compliant
- All files must be **executable** and end with a newline
- Documentation for **all** modules, classes, and functions (full sentences required)
- The Flask app must **only** use `Auth` — never directly access `DB`

**Install bcrypt:**
```bash
pip3 install bcrypt

📂 Project Structure
bash
Copy
Edit
0x03-user_authentication_service/
│
├── app.py               # Flask app and routes
├── auth.py              # Authentication logic
├── db.py                # Database helper class
├── user.py              # SQLAlchemy User model
├── main.py              # Test scripts for tasks
└── README.md            # This file


🛠 Task Overview
#	Task	Description	File
0	User model	Create User table/model	user.py
1	Create user	Add add_user method in DB	db.py
2	Find user	Find user by attributes	db.py
3	Update user	Update attributes dynamically	db.py
4	Hash password	Implement _hash_password	auth.py
5	Register user	Create register_user	auth.py
6	Basic Flask app	GET / route	app.py
7	Register endpoint	POST /users	app.py
8	Validate login	valid_login method	auth.py
9	Generate UUID	_generate_uuid	auth.py
10	Create session	Store session_id	auth.py
11	Login endpoint	POST /sessions	app.py
12	Get user by session	get_user_from_session_id	auth.py
13	Destroy session	destroy_session	auth.py
14	Logout endpoint	DELETE /sessions	app.py
15	User profile	GET /profile	app.py
16	Generate reset token	get_reset_password_token	auth.py
17	Reset token endpoint	POST /reset_password	app.py
18	Update password	update_password	auth.py
19	Update password endpoint	PUT /reset_password	app.py


🚀 Example Usage
1️⃣ Register a user

curl -XPOST localhost:5000/users \
  -d 'email=user@example.com' \
  -d 'password=StrongPass123'
Response:


{"email":"user@example.com","message":"user created"}
2️⃣ Login

curl -XPOST localhost:5000/sessions \
  -d 'email=user@example.com' \
  -d 'password=StrongPass123' -v
Response:

{"email":"user@example.com","message":"logged in"}
Cookie session_id will be set.

3️⃣ Access profile

curl -XGET localhost:5000/profile \
  -b "session_id=<session_id_here>"
Response:


{"email":"user@example.com"}
4️⃣ Request password reset

curl -XPOST localhost:5000/reset_password \
  -d 'email=user@example.com'
Response:

{"email":"user@example.com", "reset_token":"<token_here>"}
5️⃣ Update password

curl -XPUT localhost:5000/reset_password \
  -d 'email=user@example.com' \
  -d 'reset_token=<token_here>' \
  -d 'new_password=NewPass456'
Response:

{"email":"user@example.com","message":"Password updated"}
⚠ Security Notes
Always use HTTPS in production

Consider adding:

Rate limiting

CAPTCHA

Two-factor authentication (2FA)

Never store plaintext passwords

📜 License
This project is part of the ALX Backend User Data curriculum.
© 2025 ALX. All rights reserved.
