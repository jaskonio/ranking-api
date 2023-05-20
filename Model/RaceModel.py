from datetime import datetime
from typing import List
from pydantic import BaseModel
from Model.RunnerModel import RunnerModel

class RaceModel(BaseModel):
    name: str
    url: str
    order: int
    ranking: List[RunnerModel]
    sorted: bool = False

    def add_runner(self, runner):
        self.ranking.append(runner)
        self.sorted = False

    def get_ranking(self):
        if not self.sorted:
            self.__sort_runners()
            self.__set_points()
        
        return self.ranking

    def get_runners_with_points(self):
        if not self.sorted:
            self.__sort_runners()
            self.__set_points()

        return [runner for runner in self.ranking if runner.puntos != 0]

    def __sort_runners(self):
        format = "%H:%M:%S"
        # Orderna los Runner primero por finished True primero False segundo, realTime y officialTime

        runners_finished = sorted(self.ranking, key=lambda runner: (not runner.finished, datetime.strptime(runner.realTime, format), datetime.strptime(runner.officialTime, format)), reverse=False)

        self.ranking = runners_finished
        
        self.sorted = True

    def __set_points(self):
        if not self.sorted:
            self.sort_runners()

        # Asignar puntos solo a las 10 primeras personas en llegar a la meta
        for i, persona in enumerate(self.ranking[:10], start=1):
            persona.puntos = 10 - i + 1
