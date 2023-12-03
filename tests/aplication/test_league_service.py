import unittest
from unittest.mock import MagicMock
from app.aplication.league_service import LeagueService
from app.domain.model.league import League
from app.domain.model.person import Person
from app.domain.model.runner_base import RunnerBase
from app.domain.repository.igeneric_repository import IGenericRepository


class TestLeagueService(unittest.TestCase):
    def setUp(self):
        self.league_repository_mock = MagicMock(spec=IGenericRepository)
        self.race_repository_mock = MagicMock(spec=IGenericRepository)
        self.person_repository_mock = MagicMock(spec=IGenericRepository)
        self.logger_mock = MagicMock()

        self.league_service = LeagueService(
            league_repository=self.league_repository_mock,
            race_repository=self.race_repository_mock,
            person_repository=self.person_repository_mock
        )
        self.league_service.logger = self.logger_mock

    def test_get_all(self):
        # Mocking the league_repository.get_all method
        fake_league = [League()]
        self.league_repository_mock.get_all.return_value = fake_league

        # Testing the get_all method
        result = self.league_service.get_all()

        # Assertions
        self.assertEqual(result, fake_league)
        self.league_repository_mock.get_all.assert_called_once()

    def test_get_by_id(self):
        # Mocking the league_repository.get_by_id method
        expected_league = League()
        self.league_repository_mock.get_by_id.return_value = expected_league

        # Testing the get_by_id method
        result = self.league_service.get_by_id(1)

        # Assertions
        self.assertEqual(result, expected_league)
        self.league_repository_mock.get_by_id.assert_called_once_with(1)

    def test_add(self):
        # Mocking the league_repository.add and league_repository.get_by_id methods
        expected_league = League()
        self.league_repository_mock.add.return_value = 1
        self.league_repository_mock.get_by_id.return_value = expected_league

        # Testing the add method
        result = self.league_service.add(expected_league)

        # Assertions
        self.assertEqual(result, expected_league)
        self.league_repository_mock.add.assert_called_once_with(expected_league)
        self.league_repository_mock.get_by_id.assert_called_once_with(1)

    def test_add_runners(self):
        # Mocking the league_repository.get_by_id and person_repository.get_by_id methods
        expected_league = League()
        self.league_repository_mock.get_by_id.return_value = expected_league
        self.person_repository_mock.get_by_id.return_value = Person()

        # Testing the add_runners method
        result = self.league_service.add_runners("1", [RunnerBase()])

        # Assertions
        self.assertEqual(result, expected_league)
        self.league_repository_mock.get_by_id.assert_called_once_with("1")
        self.person_repository_mock.get_by_id.assert_called_once_with(RunnerBase().id)

if __name__ == '__main__':
    unittest.main()
