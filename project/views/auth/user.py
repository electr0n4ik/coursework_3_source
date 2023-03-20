from flask import request
from flask_restx import Namespace, Resource, abort
from project.container import user_service
from project.setup.api.models import user
from project.setup.api.parsers import page_parser
from project.tools.security import auth_required, compose_passwords

api = Namespace('user')


@api.route('/')
class UserView(Resource):
    """
    Представление для пользователя
    """
    @api.response(404, 'Not Found')
    @api.marshal_with(user, code=200, description='OK')
    @auth_required
    def get(self, data):
        """
        Получить информацию о пользователе
        """
        return user_service.get_user_by_login(data.get("email")), 200

    @api.response(404, 'Not Found')
    @api.marshal_with(user, code=200, description='OK')
    @auth_required
    def patch(self, data):
        """
        Изменить информацию о пользователе
        """
        update = request.json
        update["email"] = data.get("email")
        return user_service.update_user(update), 201


@api.route('/password/')
class PasswordView(Resource):
    """
    Представление для пароля пользователя
    """
    @api.response(404, 'Not Found')
    @auth_required
    def put(self, data):
        """
        Изменить пароль пользователя
        """
        old_password = request.json.get("old_password")
        new_password = request.json.get("new_password")

        if old_password != data.get("password"):
            abort(403, 'Неверно указан старый пароль')

        if old_password == new_password:
            abort(400, 'Новый пароль совпадает со старым')

        data["password"] = new_password
        return user_service.update_password(data), 200
