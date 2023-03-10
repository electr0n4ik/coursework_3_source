from project.dao.base import BaseDAO
from project.models import Genre
from project.models import Director
from project.models import User
from project.models import Movie


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre

class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director

class UsersDAO(BaseDAO[User]):
    __model__ = User

class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie
