import jwt
from flask import current_app, request
from flask_restx import abort
import base64
import hashlib
import calendar
import datetime
import hmac

from flask import current_app, request


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def compare_passwords(password_hash, other_password) -> bool:
    return hmac.compare_digest(password_hash, generate_password_hash(other_password))


def generate_tokens(email, password, password_hash=None, is_refresh=False):
    """
    Создания токенов авторизации
    """
    if email is None:
        raise abort(404)

    if not is_refresh:
        if not compare_passwords(password_hash=password_hash, other_password=password):
            abort(400, "Неверный пароль")

    data = {
        "email": email,
        "password": password
    }

    min_exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
    data["exp"] = calendar.timegm(min_exp.timetuple())
    access_token = jwt.encode(data, current_app.config['SECRET_KEY'], current_app.config['ALGORYTHM'])

    days_exp = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config['TOKEN_EXPIRE_DAYS'])
    data["exp"] = calendar.timegm(days_exp.timetuple())
    refresh_token = jwt.encode(data, current_app.config['SECRET_KEY'], algorithm=current_app.config['ALGORYTHM'])

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def approve_refresh_token(refresh_token):
    """
    Обновление токенов авторизации
    """
    data = jwt.decode(refresh_token,
                      current_app.config['SECRET_KEY'],
                      [current_app.config['ALGORYTHM']])
    login = data.get("email")

    return generate_tokens(login, None, is_refresh=True)


def auth_required(func):
    """
    Проверка авторизации
    """

    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        auth_data = request.headers['Authorization']
        token = auth_data.split("Bearer ")[-1]
        try:
            user_data = jwt.decode(jwt=token,
                                   key=current_app.config['SECRET_KEY'],
                                   algorithms=[current_app.config['ALGORYTHM']])
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, data=user_data)

    return wrapper
