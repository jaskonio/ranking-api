from typing import List
from Domain.DownloaderService import DownloaderService
from Domain.FactoryDownloader import FactoryDownloader
from Infrastructure.MongoDB.LeagueList import LeagueList
from Model.LeagueModel import LeagueModel
from Model.RaceModel import RaceModel
from Model.RunnerBaseModel import RunnerBaseModel
from Model.RunnerModel import RunnerModel

class LeagueController:
    def __init__(self, league_repository:LeagueList, downloader_service:DownloaderService):
        self.legueRepository = league_repository
        self.downloader_service = downloader_service

    def add_runner(self, new_runner: RunnerBaseModel, league_id: str):
        league = self.legueRepository.get_by_id(league_id)
        
        league.runnerParticipants.append(new_runner)
        
        self.legueRepository.update_league(league_id, league)
        
        return {'message': 'runner añadido'}

    def get_all(self):
        result = self.legueRepository.get_all()
        
        return result
        
    def create_league(self, league: LeagueModel):
        result = self.legueRepository.add_legue(league)

        return {'message': 'League creada', 'id': str(result.inserted_id)}

    def get_league(self, league_id: str):
        result = self.legueRepository.get_by_id(league_id)

        if result:
            return result
        else:
            return {'message': 'LeagueModel no encontrada'}

    def update_league(self, league_id: str, league: LeagueModel):
        result = self.legueRepository.update_league(league_id, league)

        if result.modified_count:
            return league
        else:
            return {'message': 'LeagueModel no encontrada'}

    def delete_league(self, league_id: str):
        result = self.legueRepository.delete_league(league_id)

        if result.deleted_count:
            return {'message': 'LeagueModel eliminada'}
        else:
            return {'message': 'LeagueModel no encontrada'}

    def get_final_ranking_by_league_id(self, league_id: str):
        league = self.get_league(league_id)
        return league.finalRanking

    def add_new_race_by_id(self, league_id, new_race: RaceModel):
        print("league_id: " + str(league_id))
        print("new_race: " + str(new_race))

        runners:List[RunnerModel] = self.downloader_service.download_race_data(new_race.url)

        new_race.ranking = runners
        
        league = self.get_league(league_id)
        
        league.add_race(new_race)
        
        return self.update_league(league_id, league)

    def disqualify_runner(self, bib_number:int, race_name:str, league_id: str):
        current_league = self.legueRepository.get_by_id(league_id)

        current_league.disqualify_runner_process(bib_number, race_name)

        self.legueRepository.update_league(league_id, current_league.mongo())

        return current_league