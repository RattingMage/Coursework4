from unittest.mock import MagicMock

import pytest

from dao.model.genre import Genre
from dao.genre import GenreDAO
from service.genre import GenreService

@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(None)

    Comedy = Genre(id=1, name="comedy")
    Horror = Genre(id=2, name='horror')
    Anime = Genre(id=3, name='anime')

    genre_dao.get_one = MagicMock(return_value=Anime)
    genre_dao.get_all = MagicMock(return_value=[Comedy, Horror, Anime])
    genre_dao.create = MagicMock(return_value=Genre(id=2))
    genre_dao.update = MagicMock()
    genre_dao.partially_update = MagicMock()
    genre_dao.delete = MagicMock()
    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(2)

        assert genre is not None
        assert genre.id is not None

    def test_get_all(self):
        genre = self.genre_service.get_all()

        assert len(genre) > 0

    def test_create(self):
        genre_d = {
            "name": "Woody Allen"
        }

        genre = self.genre_service.create(genre_d)

        assert genre is not None
        assert genre.id is not None

    def test_update(self):
        genre_d = {
            "id": 2,
            "name": "Woody Allen"
        }
        self.genre_service.update(genre_d)

    def test_partially_update(self):
        genre_d = {
            "id": 2,
            "name": "Ridley Scott"
        }
        self.genre_service.partially_update(genre_d)

    def test_delete(self):
        self.genre_service.delete(3)
