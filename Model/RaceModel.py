from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from Model.RunnerBaseModel import RunnerBaseModel
from Model.RunnerModel import RunnerModel

class RaceModel(BaseModel):
    name: str
    url: str
    order: int
    ranking: List[RunnerModel]
    sorted: bool = False
    runnerDisqualified: List[RunnerBaseModel] = Field(default_factory=list)

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

    def set_runner_disqualified(self, runner:RunnerBaseModel):
        self.runnerDisqualified.append(runner)
        self.sorted = False
        self.ranking = self.get_ranking()

    def __sort_runners(self):
        format = "%H:%M:%S"
        # Orderna los Runner primero por finished True primero False segundo, realTime y officialTime

        runners_finished = sorted(self.ranking, key=lambda runner: (not runner.finished, datetime.strptime(runner.realTime, format), datetime.strptime(runner.officialTime, format)), reverse=False)

        self.ranking = runners_finished
        
        self.sorted = True

    def __set_points(self):
        if not self.sorted:
            self.sort_runners()

        # excluir los runners descalificados

        bibs_number_disqualified = [ runner for runner in self.runnerDisqualified if runner.dorsal]
                                    
        # Asignar puntos solo a las 10 primeras personas en llegar a la meta
        for i, runner in enumerate(self.ranking[:10], start=1):
            if runner.dorsal in bibs_number_disqualified:
                continue

            runner.puntos = 10 - i + 1
