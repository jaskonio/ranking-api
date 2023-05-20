from typing import List
from Domain.FactoryDownloader import FactoryDownloader
from Infrastructure.MongoDB.LeagueList import LeagueList
from Model.LeagueModel import LeagueModel
from Model.RaceModel import RaceModel
from Model.RunnerModel import RunnerModel

class LeagueController:
    def __init__(self, league_repository:LeagueList, downloader_factory:FactoryDownloader):
        self.legueRepository = league_repository
        self.downloader_factory = downloader_factory

    def get_all(self):
        result = self.legueRepository.get_all()
        
        return result
        
    def create_league(self, league: LeagueModel):
        result = self.legueRepository.add_legue(league)

        return {'message': 'League creada', 'id': str(result.inserted_id)}

    def get_league(self, league_id: str):
        result = self.legueRepository.get_by_id(league_id)

        if result:
            return LeagueModel.from_mongo(result)
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

        downloader = self.downloader_factory.factory_method(new_race.url)

        runners:List[RunnerModel] = []

        if downloader != None:
            runners = downloader.race_data
            print("Se ha descargado con exito")
        else:
            return {'message': 'Process factory downloader'}           

        # Se crea el objeto carrera y se guarda en base de datos
        new_race.ranking = runners
        
        league = self.get_league(league_id)
        
        league.add_race(new_race)
        
        return self.update_league(league_id, league)
