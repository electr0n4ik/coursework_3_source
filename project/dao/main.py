from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc
from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO
from project.models import *
from project.tools.security import generate_password_hash


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class MoviesDAO(BaseDAO[Movie]):
    """
    DAO для фильмов
    """
    __model__ = Movie

    def get_all_by_order(self, page, filter):
        """
        Метод для получения всех фильмов от новых к старым
        """
        stmt: BaseQuery = self._db_session.query(self.__model__)
        if filter:
            stmt = stmt.order_by(desc(self.__model__.year))
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()


class UsersDAO(BaseDAO[User]):
    """
    DAO для пользователей
    """
    __model__ = User

    def create(self, login, password):
        """
        Метод создания нового пользователя
        """
        try:
            self._db_session.add(
                User(
                    email=login,
                    password=generate_password_hash(password)
                )
            )
            self._db_session.commit()
            print('Пользователь добавлен')
        except Exception as e:
            print(e)
            self._db_session.rollback()

    def get_user_by_login(self, login):
        """
        Метод получения пользователя по логину
        """
        try:
            stmt = self._db_session.query(self.__model__).filter(self.__model__.email == login).one()
            return stmt
        except Exception as e:
            print(e)

    def update(self, login, data):
        """
        Метод для обновления данных о пользователе
        """
        try:
            self._db_session.query(self.__model__).filter(self.__model__.email == login).update(data)
            self._db_session.commit()
        except Exception as e:
            print(e)
            self._db_session.rollback()
