import base64
import hashlib

from flask import request, abort
import jwt
from constants import secret, algo, PWD_SALT, PWD_ITERATIONS


def generate_password(password):  # функция перегоняет пароль в хэш
    hash_digest = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        PWD_SALT,
        PWD_ITERATIONS
    )
    return base64.b64encode(hash_digest)


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, secret, algorithms=[algo])
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            user = jwt.decode(token, secret, algorithms=[algo])
            role = user.get("role")
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        if role != "admin":
            abort(403)
        return func(*args, **kwargs)

    return wrapper
