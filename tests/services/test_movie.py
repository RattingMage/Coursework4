from unittest.mock import MagicMock

import pytest

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)

    Crime_novel = Movie(id=1, title="Crime novel")
    Gentlemen = Movie(id=2, title="Gentlemen")
    Betman = Movie(id=3, title="Betman")

    movie_dao.get_one = MagicMock(return_value=Gentlemen)
    movie_dao.get_all = MagicMock(return_value=[Crime_novel, Gentlemen, Betman])
    movie_dao.create = MagicMock(return_value=Movie(id=2))
    movie_dao.update = MagicMock()
    movie_dao.partially_update = MagicMock()
    movie_dao.delete = MagicMock()
    return movie_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(2)

        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movie = self.movie_service.get_all()

        assert len(movie) > 0

    def test_create(self):
        movie_d = {
            "name": "Woody Allen"
        }

        movie = self.movie_service.create(movie_d)

        assert movie is not None
        assert movie.id is not None

    def test_update(self):
        movie_d = {
            "id": 2,
            "name": "Woody Allen"
        }
        self.movie_service.update(movie_d)

    def test_partially_update(self):
        movie_d = {
            "id": 2,
            "name": "Ridley Scott"
        }
        self.movie_service.partially_update(movie_d)

    def test_delete(self):
        self.movie_service.delete(3)
