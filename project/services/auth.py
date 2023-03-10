import calendar
import datetime

import jwt
from constants import SECRET, ALGO, TOKEN_EXPIRE_MINUTES, TOKEN_EXPIRE_DAYS
from flask_restx import abort
from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):
        user = self.user_service.get_by_username(username)

        if user is None:
            raise abort(404)

        if not is_refresh:
            print(user.password)
            print(password)
            if not self.user_service.compare_passwords(user.password, password):
                abort(400)

        data = {
            "username": user.username,
            "role": user.role
        }

        min_exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        data["exp"] = calendar.timegm(min_exp.timetuple())
        access_token = jwt.encode(data, SECRET, ALGO)

        days_exp = datetime.datetime.utcnow() + datetime.timedelta(days=TOKEN_EXPIRE_DAYS)
        data["exp"] = calendar.timegm(days_exp.timetuple())
        refresh_token = jwt.encode(data, SECRET, algorithm=ALGO)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(refresh_token, SECRET, [ALGO])
        username = data.get("username")

        return self.generate_tokens(username, None, is_refresh=True)