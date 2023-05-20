from typing import List
from Domain.FactoryDownloader import FactoryDownloader
from Infrastructure.MongoDB.LeagueList import LeagueList
from Model.LeagueModel import LeagueModel
from Model.RaceModel import RaceModel
from Model.RunnerModel import RunnerModel

factory_downloader = FactoryDownloader()

class LeagueController:
    def __init__(self) -> None:
        self.legueRepository = LeagueList()
        pass

    def create_league(self, league: LeagueModel):
        result = self.legueRepository.add_legue(league)

        return {'message': 'League creada', 'id': str(result.inserted_id)}

    def get_league(self, league_id: str):
        result = self.legueRepository.get_legue_by_id(league_id)

        if result:
            return LeagueModel(id=result['_id'], name=result['name'], races=result['races'], finalRanking=result['finalRanking'])
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

    def calcular_ranking_league(self, league_id: str):
        league = self.get_league(league_id)
        return self.calcular_ranking_by_league(league)

    def calcular_ranking_by_league(self, league: LeagueModel):
        if isinstance(league, LeagueModel) and 'carreras' in league:
            ranking_league = {}

            for race in league.get_races():
                for runner in race.get_ranking():
                    if runner.name not in ranking_league:
                        ranking_league[runner.name] = RunnerModel(**runner.dict())
                    else:
                        ranking_league[runner.name].puntos += runner.puntos
                        ranking_league[runner.name].posiciones_ant.extend(runner.posiciones_ant)

            sorted_ranking = sorted(ranking_league.values(), key=lambda runner: (runner.puntos, sum(runner.posiciones_ant) / len(runner.posiciones_ant)), reverse=True)
            return {'ranking_league': sorted_ranking}
        else:
            return {'message': 'Liga no encontrada o sin carreras registradas'}

    def add_new_race_by_id(self, league_id, new_race: RaceModel):
        print("league_id: " + str(league_id))
        print("new_race: " + str(new_race))

        downloader = factory_downloader.factory_method(new_race.url)

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
