from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from .runner_base_model import RunnerBaseModel
from .runner_model import RunnerModel

class RaceModel(BaseModel):
    name: str
    url: str
    order: int
    ranking: List[RunnerModel] = Field(default_factory=list)
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

    def set_runners_disqualified(self, runners:List[RunnerBaseModel]):
        self.runnerDisqualified.extend(runners)
        self.sorted = False
        self.update_ranking()            

    def set_runner_disqualified(self, runner:RunnerBaseModel):
        self.runnerDisqualified.append(runner)
        self.sorted = False
        self.update_ranking()

    def update_ranking(self):
        if not self.sorted:
            self.__sort_runners()
            self.__set_points()

    def __sort_runners(self):
        format = "%H:%M:%S"
        # Orderna los Runner primero por finished True primero False segundo, realTime y officialTime

        runners_finished = sorted(self.ranking, key=lambda runner: (not runner.finished, datetime.strptime(runner.realTime, format), datetime.strptime(runner.officialTime, format)), reverse=False)

        self.ranking = runners_finished
        
        self.sorted = True

    def __set_points(self):
        if not self.sorted:
            self.__sort_runners()

        # excluir los runners descalificados

        disqualified_bibs  = [ runner for runner in self.runnerDisqualified if runner.dorsal]

        # Asignar puntos como en la F1
        points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

        for i, runner in enumerate(self.ranking):
            if runner.dorsal in disqualified_bibs:
                continue

            if i < len(points):
                runner.puntos = points[i]
            else:
                runner.puntos = 0
