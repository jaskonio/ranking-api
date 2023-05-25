import unittest
from unittest.mock import Mock
from app.controller.LeagueController import LeagueController
from app.infrastructure.mongoDB.LeagueList import LeagueList
from app.domain.DownloaderService import DownloaderService
from tests.utils.builder.LeagueModelBuilder import LeagueModelBuilder
from tests.utils.builder.RaceModelBuilder import RaceModelBuilder
from tests.utils.builder.RunnerBaseModelBuilder import RunnerBaseModelBuilder
from tests.utils.builder.RunnerModelBuilder import RunnerModelBuilder

class LeagueControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_league_repository = Mock(spec=LeagueList)
        self.mock_downloader_service = Mock(spec=DownloaderService)
        self.controller = LeagueController(self.mock_league_repository, self.mock_downloader_service)

        self.runner_base_model_builder = RunnerBaseModelBuilder()
        self.league_model_builder = LeagueModelBuilder()
        self.race_model_builder = RaceModelBuilder()
        self.runner_model_builder = RunnerModelBuilder()

    def test_add_runner_success(self):
        league_id = "123"

        new_runner = self.runner_base_model_builder.create_new_runner_base_fake()
        league = self.league_model_builder.create_league_model_fake()

        self.mock_league_repository.get_by_id.return_value = league

        result = self.controller.add_runner(new_runner, league_id)

        self.assertEqual(result, {'message': 'Runner añadido correctamente.'})
        self.mock_league_repository.get_by_id.assert_called_once_with(league_id)
        self.mock_league_repository.update_league.assert_called_once_with(league_id, league)

    def test_add_runner_league_not_found(self):
        league_id = "123"
        new_runner = self.runner_base_model_builder.create_new_runner_base_fake()
        self.mock_league_repository.get_by_id.return_value = None

        result = self.controller.add_runner(new_runner, league_id)

        self.assertEqual(result, {'message': 'League not found.'})
        self.mock_league_repository.get_by_id.assert_called_once_with(league_id)
        self.mock_league_repository.update_league.assert_not_called()

    def test_add_new_race_by_id_success(self):
        league_id = "123"
        
        new_race = self.race_model_builder.create_race_moldel_fake()

        runners = self.runner_model_builder.create_runners_model_fake(4)
        self.mock_downloader_service.download_race_data.return_value = runners

        league = self.league_model_builder.create_league_model_fake(runnerParticipants=self.runner_base_model_builder.create_runners_base_fake(4))
        self.mock_league_repository.get_by_id.return_value = league

        result = self.controller.add_new_race_by_id(league_id, new_race)

        self.assertEqual(result, {'message': 'Carrera añadida correctamente.'})
        self.mock_downloader_service.download_race_data.assert_called_once_with(new_race.url)
        self.assertEqual(new_race.ranking, runners)
        self.mock_league_repository.get_by_id.assert_called_once_with(league_id)
        self.mock_league_repository.update_league.assert_called_once_with(league_id, league)

    def test_add_new_race_by_id_runners_empty(self):
        league_id = "123"

        new_race = self.race_model_builder.create_race_moldel_fake()
        self.mock_downloader_service.download_race_data.return_value = []

        league = self.league_model_builder.create_league_model_fake()
        self.mock_league_repository.get_by_id.return_value = league

        result = self.controller.add_new_race_by_id(league_id, new_race)

        self.assertEqual(result, {'message': 'Error al descargar los datos de la carrera.'})
        self.mock_downloader_service.download_race_data.assert_called_once_with(new_race.url)
        self.assertEqual(new_race.ranking, [])

    def test_add_new_race_by_id_league_not_found(self):
        league_id = "123"
        new_race = self.race_model_builder.create_race_moldel_fake()
        runners = self.runner_model_builder.create_runners_model_fake(2)
        self.mock_downloader_service.download_race_data.return_value = runners
        self.mock_league_repository.get_by_id.return_value = None

        result = self.controller.add_new_race_by_id(league_id, new_race)

        self.assertEqual(result, {'message': 'No se encontró la Liga especificada.'})

    def test_disqualify_runner_success(self):
        bib_number = 1
        race_name = "Race Name 1"
        league_id = "123"

        rankings_fake = self.runner_base_model_builder.create_runners_base_fake(4)
        races_fake = [self.race_model_builder.create_race_moldel_fake(ranking=rankings_fake)]

        current_league = self.league_model_builder.create_league_model_fake(name=league_id,
                                                                            races=races_fake,
                                                                            runnerParticipants=self.runner_base_model_builder.create_runners_base_fake(4))
        self.mock_league_repository.get_by_id.return_value = current_league

        result = self.controller.disqualify_runner(bib_number, race_name, league_id)

        self.assertEqual(result, current_league)
        self.mock_league_repository.get_by_id.assert_called_once_with(league_id)        
        self.mock_league_repository.update_league.assert_called_once_with(league_id, current_league)

if __name__ == "__main__":
    unittest.main()
