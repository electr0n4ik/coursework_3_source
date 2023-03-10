from project.dao.genre import GenreDAO
from project.dao.director import DirectorDAO
from project.dao.user import UserDAO
from project.dao.movie import MovieDAO

from project.services.genre import GenreService
from project.services.director import DirectorService
from project.services.user import UserService
from project.services.movie import MovieService

from project.setup.db import db

# DAO
genre_dao = GenreDAO(db.session)
director_dao = DirectorDAO(db.session)
user_dao = UserDAO(db.session)
movie_dao = MovieDAO(db.session)

# Services
genre_service = GenreService(dao=genre_dao)
director_service = DirectorService(dao=director_dao)
user_service = UserService(dao=user_dao)
movie_service = MovieService(dao=movie_dao)
