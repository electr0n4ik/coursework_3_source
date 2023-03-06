from unittest.mock import MagicMock
import pytest
from dao.movie import MovieDAO
from dao.model.movie import Movie
from service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)

    movie_1 = Movie(
        id=1,
        title="movie_1",
        description="first movie for test",
        trailer="testmovie1.com",
        year=2023,
        rating=10,
        genre_id=1,
        genre="Comedy",
        director_id=1,
        director="putin"
    )
    movie_2 = Movie(
        id=2,
        title="movie_2",
        description="second movie for test",
        trailer="testmovie2.com",
        year=2023,
        rating=10,
        genre_id=1,
        genre="Comedy",
        director_id=2,
        director="putin"
    )
    movie_3 = Movie(
        id=3,
        title="movie_3",
        description="first movie for test",
        trailer="testmovie3.com",
        year=2023,
        rating=10,
        genre_id=3,
        genre="Comedy",
        director_id=3,
        director="putin"
    )

    movie_dao.get_one = MagicMock(return_value=movie_1)
    movie_dao.get_all = MagicMock(return_value=[movie_1, movie_2, movie_3])
    movie_dao.create = MagicMock(return_value=Movie(id=4))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()
    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)

        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()

        assert len(movies) > 0

    def test_create(self):
        movie_d = {
            "name": "Other movie"
        }
        movie = self.movie_service.create(movie_d)

        assert movie.id is not None

    def test_delete(self):
        self.movie_service.delete(1)

    def test_update(self):
        movie_d = {
            "id": 2,
            "name": "Movie 2 upd"
        }

        self.movie_service.update(movie_d)
