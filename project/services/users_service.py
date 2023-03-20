from typing import Optional

from project.dao.main import UsersDAO
from project.exceptions import ItemNotFound
from project.models import User
from project.tools.security import generate_password_hash, generate_tokens, approve_refresh_token


class UsersService:
    def __init__(self, dao: UsersDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} does not exists.')

    def get_all(self, page: Optional[int] = None) -> list[User]:
        return self.dao.get_all(page=page)

    def get_user_by_login(self, login: str) -> User:
        if user := self.dao.get_user_by_login(login):
            return user
        raise ItemNotFound(f'User with pk={login} does not exists.')

    def create(self, login, password):
        self.dao.create(login, password)

    def check_in(self, login, password):
        user = self.get_user_by_login(login)
        return generate_tokens(email=user.email, password=password, password_hash=user.password)

    def update_token(self, refresh_token):
        return approve_refresh_token(refresh_token)

    def update_user(self, data):
        user = self.get_user_by_login(data.get('email'))
        self.dao.update(login=user.email, data=data)
        return user

    def update_password(self, data):
        user = self.get_user_by_login(data.get('email'))
        data["password"] = generate_password_hash(data.get("password"))
        self.dao.update(login=user.email, data={"password": data["password"]})
        return "Пароль обновлен"
