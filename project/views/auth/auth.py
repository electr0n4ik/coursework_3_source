from flask import request
from flask_restx import Namespace, Resource, abort
from project.container import user_service

api = Namespace('auth')


@api.route('/register/')
class RegisterView(Resource):
    """
    Регистрация пользователей
    """
    def post(self):
        """
        Создание нового пользователя
        """
        data = request.json

        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user_service.get_user_by_login(email)
                return "Пользователь с данным логином уже существует", 401
            except Exception:
                return user_service.create(email, password), 201
        else:
            return "Неверный ввод данных", 401


@api.route('/login/')
class LoginView(Resource):
    """
    Вход пользователя
    """
    @api.response(404, 'Not Found')
    def post(self):
        """
        Получение токенов авторизации
        """
        data = request.json

        email = data.get('email')
        password = data.get('password')

        if email and password:
            return user_service.check_in(email, password), 201
        else:
            return "Неверный ввод данных", 401

    @api.response(404, 'Not Found')
    def put(self):
        """
        Обновление токенов авторизации
        """
        data = request.json
        refresh_token = data.get('refresh_token')

        if not refresh_token:
            abort(400)

        return user_service.update_token(refresh_token), 201
