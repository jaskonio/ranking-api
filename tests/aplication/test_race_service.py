import copy
import unittest
from unittest.mock import Mock
from app.aplication.race_service import RaceService
from app.domain.model.runner_race_ranking import RunnerRaceRanking
from app.domain.repository.idownloader_race_data import RaceDownloaderOptions
from app.domain.repository.igeneric_repository import IGenericRepository
from app.domain.services.downloader_runners_service import DownloaderRunnersService
from tests.utils.race_builder import RaceBuilder

class TestRaceService(unittest.TestCase):
    def setUp(self):
        self.race_repository_mock = Mock(spec=IGenericRepository)
        self.person_repository_mock = Mock(spec=IGenericRepository)
        self.downloader_service_mock = Mock(spec=DownloaderRunnersService)
        self.race_service = RaceService(
            self.race_repository_mock,
            self.person_repository_mock,
            self.downloader_service_mock
        )

    def test_get_all_when_race_repository_mock_return_0(self):
        # Mock the repository behavior
        expected_races = []
        self.race_repository_mock.get_all.return_value = expected_races

        actual_races = self.race_service.get_all()

        self.assertEqual(actual_races, expected_races)

    def test_get_all_when_race_repository_mock_return_1(self):
        # Mock the repository behavior
        expected_races = [RaceBuilder().build()]
        self.race_repository_mock.get_all.return_value = expected_races

        actual_races = self.race_service.get_all()

        self.assertEqual(actual_races, expected_races)

    def test_get_by_id(self):
        # Mock the repository behavior
        expected_race = [RaceBuilder().build()]
        self.race_repository_mock.get_by_id.return_value = expected_race

        actual_race = self.race_service.get_by_id(expected_race[0].id)

        self.assertEqual(actual_race, expected_race)

    def test_processed_runners(self):
        # Mock the downloader service behavior
        runners = [RunnerRaceRanking(id='1', first_name='Runner 1'), RunnerRaceRanking(id='2', first_name='Runner 2')]
        self.downloader_service_mock.get_runners_by_persons.return_value = runners

        # Mock the repository behavior
        new_race = RaceBuilder().build()
        expected_new_race = copy.deepcopy(new_race)

        self.race_repository_mock.add.return_value = new_race.id
        self.race_repository_mock.get_by_id.return_value = new_race

        added_race = self.race_service.processed_runners(new_race.id)

        self.assertEqual(added_race.id, expected_new_race.id)
        self.assertEqual(added_race.name, expected_new_race.name)
        self.assertEqual(added_race.raw_ranking, runners)
        self.assertEqual(added_race.is_sorted, False)
        self.assertEqual(added_race.order, 0)
        self.assertEqual(added_race.ranking, [])
        self.assertEqual(added_race.participants, [])
