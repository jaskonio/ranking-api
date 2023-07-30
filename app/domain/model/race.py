from datetime import datetime
from typing import List
from app.domain.model.race_base import RaceBase
from app.domain.model.runner_race_ranking import RunnerRaceRanking


class Race(RaceBase):
    def __init__(self, id, name: str='', url: str='', ranking: List[RunnerRaceRanking] = []
                 , order:int = 0, is_sorted: bool = False):
        super().__init__(id, name, url, ranking)
        self.order = order
        self.is_sorted = is_sorted

    def add_runners(self, runners:RunnerRaceRanking):
        for runner in runners:
            self.add_runner(runner)

    def add_runner(self, runner):
        self.ranking.append(runner)
        self.is_sorted = False

    def get_ranking(self):
        if not self.is_sorted:
            self.__sort_runners()
            self.set_points()

        return self.ranking

    def set_ranking(self, ranking:List[RunnerRaceRanking]):
        if not self.is_sorted:
            self.__sort_runners()
            self.set_points()

        self.ranking = ranking

    def get_runners_with_points(self):
        if not self.is_sorted:
            self.__sort_runners()
            self.set_points()

        return [runner for runner in self.ranking if runner.points != 0]

    def set_runners_disqualified(self, runners:List[RunnerRaceRanking]):
        for runner in runners:
            self.set_runner_disqualified(runner)

    def set_runner_disqualified(self, current_runner:RunnerRaceRanking):
        for runner in self.ranking:
            if runner == current_runner:
                runner.is_disqualified = True

        self.is_sorted = False
        self.update_ranking()

    def update_ranking(self):
        if not self.is_sorted:
            self.__sort_runners()
            self.set_points()

    def __sort_runners(self):
        time_format = "%H:%M:%S"

        # Orderna los Runner primero por finished True
        # primero False segundo, realTime y officialTime
        runners_finished = sorted(self.ranking,
                                    key=lambda runner: (not runner.finished,
                                                datetime.strptime(runner.real_time, time_format)),
                                    reverse=False)

        self.ranking = runners_finished

        self.is_sorted = True

    def set_points(self):
        if not self.is_sorted:
            self.__sort_runners()

        # excluir los runners descalificados

        disqualified_bibs = []

        for runner in self.ranking:
            if runner.is_disqualified:
                disqualified_bibs.append(runner.dorsal)

        # Asignar puntos como en la F1
        points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1, 0.75, 0.50, 0.25, 0.10, 0.05]
        point_index = 0

        for runner in self.ranking:
            if runner.dorsal in disqualified_bibs:
                continue

            if point_index < len(points):
                runner.points = points[point_index]
            else:
                runner.points = 0

            runner.position = point_index + 1

            point_index = point_index + 1
