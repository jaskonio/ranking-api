"""_summary_

Returns:
    _type_: _description_
"""
from datetime import datetime
from typing import List
from pydantic import Field
from app.model.BaseMongoModel import BaseMongoModel
from app.model.OID import OID
from app.model.runner_base_model import RunnerBaseModel
from app.model.runner_model import RunnerModel

class RaceModel(BaseMongoModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_

    Returns:
        _type_: _description_
    """
    id: OID = Field(default_factory=OID)
    name: str
    url: str
    order: int
    ranking: List[RunnerModel] = Field(default_factory=list)
    sorted: bool = False
    runnerDisqualified: List[RunnerBaseModel] = Field(default_factory=list)

    def add_runner(self, runner):
        """_summary_

        Args:
            runner (_type_): _description_
        """
        self.ranking.append(runner)
        self.sorted = False

    def get_ranking(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        if not self.sorted:
            self.__sort_runners()
            self.__set_points()

        return self.ranking

    def get_runners_with_points(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        if not self.sorted:
            self.__sort_runners()
            self.set_points()

        return [runner for runner in self.ranking if runner.puntos != 0]

    def set_runners_disqualified(self, runners:List[RunnerBaseModel]):
        """_summary_

        Args:
            runners (List[RunnerBaseModel]): _description_
        """
        self.runnerDisqualified.extend(runners)
        self.sorted = False

    def set_runner_disqualified(self, runner:RunnerBaseModel):
        """_summary_

        Args:
            runner (RunnerBaseModel): _description_
        """
        self.runnerDisqualified.append(runner)
        self.sorted = False
        self.update_ranking()

    def update_ranking(self):
        """_summary_
        """
        if not self.sorted:
            self.__sort_runners()
            self.__set_points()

    def __sort_runners(self):
        format = "%H:%M:%S"

        # Orderna los Runner primero por finished True
        # primero False segundo, realTime y officialTime
        runners_finished = sorted(self.ranking,
                                    key=lambda runner: (not runner.finished,
                                                datetime.strptime(runner.realTime, format),
                                                datetime.strptime(runner.officialTime, format)),
                                    reverse=False)

        self.ranking = runners_finished

        self.sorted = True

    def set_points(self):
        if not self.sorted:
            self.__sort_runners()

        # excluir los runners descalificados

        disqualified_bibs  = [ runner for runner in self.runnerDisqualified if runner.dorsal]

        # Asignar puntos como en la F1
        points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1, 0.75, 0.50, 0.25, 0.10, 0.05]
        point_index = 0

        for runner in self.ranking:
            if runner.dorsal in disqualified_bibs:
                continue

            if point_index < len(points):
                runner.puntos = points[point_index]
            else:
                runner.puntos = 0

            runner.position = point_index + 1

            point_index = point_index + 1
