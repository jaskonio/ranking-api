from typing import List
from pydantic import BaseModel, Field
from Model.RaceModel import RaceModel
from Model.RunnerModel import RunnerModel
from bson import ObjectId

class LeagueModel(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId())
    name: str
    races: List[RaceModel] = Field(default_factory=[])
    finalRanking: List[RunnerModel] = Field(default_factory=[])

    def get_races(self):
        return sorted(self.races, key=lambda race: (race.order))

    def add_race(self, new_race: RaceModel):
        self.races.append(new_race)
        self.calculate_final_ranking()

    def calculate_final_ranking(self):
        ranking_league = {}

        for race in self.get_races():
            runners = race.get_runners_with_points()
            for runner in runners:
                if runner.name not in ranking_league:
                    ranking_league[runner.name] = RunnerModel(**runner.dict())
                else:
                    ranking_league[runner.name].puntos += runner.puntos
                    ranking_league[runner.name].posiciones_ant.extend(runner.posiciones_ant)

        self.finalRanking = sorted(ranking_league.values(), key=lambda runner: (runner.puntos, self.__order_runner(runner)), reverse=True)

    def __order_runner(self, runner):
        try:
            return sum(runner.posiciones_ant) / len(runner.posiciones_ant)
        except :
            return 0
        
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        