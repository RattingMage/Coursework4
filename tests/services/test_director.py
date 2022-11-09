from unittest.mock import MagicMock

import pytest

from dao.model.director import Director
from dao.director import DirectorDAO
from service.director import DirectorService


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(None)

    Tarantino = Director(id=1, name="Quentin Tarantino")
    Richi = Director(id=2, name="Guy Ritchie")
    Burton = Director(id=3, name="Tim Burton")

    director_dao.get_one = MagicMock(return_value=Tarantino)
    director_dao.get_all = MagicMock(return_value=[Tarantino, Richi, Burton])
    director_dao.create = MagicMock(return_value=Director(id=3))
    director_dao.update = MagicMock()
    director_dao.partially_update = MagicMock()
    director_dao.delete = MagicMock()
    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(2)

        assert director is not None
        assert director.id is not None

    def test_get_all(self):
        director = self.director_service.get_all()

        assert len(director) > 0

    def test_create(self):
        director_d = {
            "name": "Woody Allen"
        }

        director = self.director_service.create(director_d)

        assert director is not None
        assert director.id is not None

    def test_update(self):
        director_d = {
            "id": 2,
            "name": "Woody Allen"
        }
        self.director_service.update(director_d)

    def test_partially_update(self):
        director_d = {
            "id": 2,
            "name": "Ridley Scott"
        }
        self.director_service.partially_update(director_d)

    def test_delete(self):
        self.director_service.delete(3)
