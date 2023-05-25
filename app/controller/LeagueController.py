import logging
from typing import List
from ..infrastructure.mongoDB.LeagueList import LeagueList
from ..domain.DownloaderService import DownloaderService
from ..model.LeagueModel import LeagueModel
from ..model.RaceModel import RaceModel
from ..model.RunnerBaseModel import RunnerBaseModel
from ..model.RunnerModel import RunnerModel

class LeagueController:
    def __init__(self, league_repository:LeagueList, downloader_service:DownloaderService):
        self.league_repository = league_repository
        self.downloader_service = downloader_service
        self.logger = logging.getLogger(__name__)

    def add_runner(self, new_runner: RunnerBaseModel, league_id: str):
        try:
            league = self.league_repository.get_by_id(league_id)

            if league:
                league.add_runner(new_runner)
                self.league_repository.update_league(league_id, league)
                self.logger.info("Runner added successfully.")
                return {'message': 'Runner añadido correctamente.'}
            else:
                self.logger.error("League not found.")
                return {'message': 'League not found.'}
        except Exception as e:
            self.logger.error(f"Error adding runner: {str(e)}")
            return {'message': 'An error occurred while adding the runner.'}

    def get_all(self):
        try:
            return self.league_repository.get_all()
        except Exception as e:
            self.logger.error(f"Error retrieving all leagues: {str(e)}")
            return {'message': 'An error occurred while retrieving all leagues.'}

    def create_league(self, league: LeagueModel):
        result = self.league_repository.add_legue(league)
        return {'message': 'Liga creada correctamente.', 'id': str(result.inserted_id)}

    def get_league(self, league_id: str):
        result = self.league_repository.get_by_id(league_id)

        if result:
            return result
        else:
            return {'message': 'No se encontró la LigaModel especificada.'}

    def update_league(self, league_id: str, league: LeagueModel):
        result = self.league_repository.update_league(league_id, league)

        if result.modified_count:
            return league
        else:
            return {'message': 'No se encontró la LigaModel especificada.'}

    def delete_league(self, league_id: str):
        result = self.league_repository.delete_league(league_id)

        if result.deleted_count:
            return {'message': 'LigaModel eliminada correctamente.'}
        else:
            return {'message': 'No se encontró la LigaModel especificada.'}

    def get_final_ranking_by_league_id(self, league_id: str):
        league = self.league_repository.get_by_id(league_id)

        if league:
            return league.finalRanking
        else:
            return {'message': 'No se encontró la LigaModel especificada.'}

    def add_new_race_by_id(self, league_id, new_race: RaceModel):
        league = self.league_repository.get_by_id(league_id)

        if not league:
            return {'message': 'No se encontró la Liga especificada.'}

        runners:List[RunnerModel] = self.downloader_service.download_race_data(new_race.url)

        if runners:
            new_race.ranking.extend(runners)

            if league:
                league.add_race(new_race)
                self.update_league(league_id, league)
                return {'message': 'Carrera añadida correctamente.'}
            else:
                return {'message': 'No se encontró la LigaModel especificada.'}
        else:
            return {'message': 'Error al descargar los datos de la carrera.'}

    def disqualify_runner(self, bib_number:int, race_name:str, league_id: str):
        current_league = self.league_repository.get_by_id(league_id)

        if current_league:
            if len(current_league.races) == 0:
                return {'message': 'No se encontró la carrera especificada.'}

            current_league.disqualify_runner_process(bib_number, race_name)
            self.league_repository.update_league(league_id, current_league)
            return current_league
        else:
            return {'message': 'No se encontró la LigaModel especificada.'}
