import logging
from typing import List
from pymongo import errors
from app.infrastructure.mongoDB.LeagueList import LeagueList
from app.domain.DownloaderService import DownloaderService
from app.model.LeagueModel import LeagueModel
from app.model.RaceModel import RaceModel
from app.model.RunnerBaseModel import RunnerBaseModel
from app.model.RunnerModel import RunnerModel


class LeagueController:
    '''
        This class managment League Model
    '''
    def __init__(self, league_repository:LeagueList, downloader_service:DownloaderService):
        '''
        Initializes an instance of LeagueController.

        Args:
            league_repository (LeagueList): The repository for league data.
            downloader_service (DownloaderService): The service used for downloading race data.
        '''
        self.league_repository = league_repository
        self.downloader_service = downloader_service
        self.logger = logging.getLogger(__name__)

    def add_runner(self, new_runner: RunnerBaseModel, league_id: str):
        '''
        Adds a new runner to a league.

        Args:
            new_runner (RunnerBaseModel): The runner to be added.
            league_id (str): The ID of the league.

        Returns:
            dict: A dictionary containing a success message or an
            error message if an exception occurred.
        '''
        try:
            league = self.league_repository.get_by_id(league_id)

            message = ''

            if league:
                league.add_runner(new_runner)
                self.league_repository.update_league(league_id, league)
                self.logger.info("Runner added successfully.")
                message = 'Runner añadido correctamente.'
            else:
                self.logger.error("League not found.")
                message = 'League not found.'
            return {'message': message}
        except errors.NetworkTimeout as network_timeout:
            self.logger.error('Error adding runner: %', network_timeout)

        except Exception as e:
            self.logger.error("Error adding runner: {}".format(str(e)))
            return {'message': 'An error occurred while adding the runner.'}

    def get_all(self):
        '''
        Retrieves all leagues.

        Returns:
            list: A list of all leagues or an error message if an exception occurred.
        '''
        try:
            return self.league_repository.get_all()
        except Exception as e:
            self.logger.error(f"Error retrieving all leagues: {str(e)}")
            return {'message': 'An error occurred while retrieving all leagues.'}

    def create_league(self, league: LeagueModel):
        '''
        Creates a new league.

        Args:
            league (LeagueModel): The league to be created.

        Returns:
            dict: A dictionary containing a success message and the ID of the created league.
        '''
        result = self.league_repository.add_legue(league)
        return {'message': 'Liga creada correctamente.', 'id': str(result.inserted_id)}

    def get_league(self, league_id: str):
        '''
        Retrieves a league by its ID.

        Args:
            league_id (str): The ID of the league.

        Returns:
            LeagueModel: The retrieved league or an error message if the league was not found.
        '''
        result = self.league_repository.get_by_id(league_id)

        if not result:
            result = {'message': 'No se encontró la LigaModel especificada.'}

        return result

    def update_league(self, league_id: str, league: LeagueModel):
        '''
        Updates a league.

        Args:
            league_id (str): The ID of the league.
            league (LeagueModel): The updated league.

        Returns:
            Union[LeagueModel, dict]: The updated league if it was found and updated,
            or an error message if the league was not found.
        '''
        result = self.league_repository.update_league(league_id, league)

        if result.modified_count:
            return league
        else:
            return {'message': 'No se encontró la LigaModel especificada.'}

    def delete_league(self, league_id: str):
        '''
        Deletes a league.

        Args:
            league_id (str): The ID of the league.

        Returns:
            dict: A dictionary containing a success message
            if the league was deleted or an error message if the league was not found.
        '''
        result = self.league_repository.delete_league(league_id)

        message = ''
        if result.deleted_count:
            message = 'LigaModel eliminada correctamente.'
        else:
            message = 'No se encontró la LigaModel especificada.'

        return {'message': message}

    def get_final_ranking_by_league_id(self, league_id: str):
        '''
        Retrieves the final ranking of a league by its ID.

        Args:
            league_id (str): The ID of the league.

        Returns:
            Union[list, dict]: The final ranking of the league if it was found,
            or an error message if the league was not found.
        '''
        league = self.league_repository.get_by_id(league_id)

        if league:
            return league.finalRanking
        else:
            return {'message': 'No se encontró la LigaModel especificada.'}

    def add_new_race_by_id(self, league_id, new_race: RaceModel):
        '''
        Adds a new race to a league by its ID.

        Args:
            league_id (str): The ID of the league.
            new_race (RaceModel): The race to be added.

        Returns:
            dict: A dictionary containing a success message if the race was added,
            or an error message if the league or race was not found or
            if there was an error downloading the race data.
        '''
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
        '''
        Disqualifies a runner in a race of a league.

        Args:
            bib_number (int): The bib number of the runner.
            race_name (str): The name of the race.
            league_id (str): The ID of the league.

        Returns:
            Union[LeagueModel, dict]: The updated league with the disqualified runner
            if the league and race were found, or an error message
            if the league or race was not found.
        '''
        current_league = self.league_repository.get_by_id(league_id)

        if current_league:
            if len(current_league.races) == 0:
                return {'message': 'No se encontró la carrera especificada.'}

            current_league.disqualify_runner_process(bib_number, race_name)
            self.league_repository.update_league(league_id, current_league)
            return current_league
        else:
            return {'message': 'No se encontró la LigaModel especificada.'}
