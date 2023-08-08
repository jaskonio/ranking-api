from typing import List
from app.core.mapper_utils import dicts_to_class
from app.domain.model.race_base import RaceBase
from app.domain.model.runner import Runner
from app.domain.model.runner_race_ranking import RunnerRaceRanking


class Race(RaceBase):
    def __init__(self, id, name: str='', url: str='', raw_ranking: List[RunnerRaceRanking] = None
                 , order:int = 0, is_sorted: bool = False, ranking: List[RunnerRaceRanking] = None
                 , runners: List[Runner] = None):
        super().__init__(id, name, url, raw_ranking)
        self.order = order
        self.is_sorted = is_sorted
        self.ranking:List[RunnerRaceRanking] = [] if ranking is None else dicts_to_class(RunnerRaceRanking, ranking)
        self.runners:List[Runner] = [] if runners is None else dicts_to_class(Runner, runners)

    def add_runners(self, runners:List[RunnerRaceRanking]):
        for runner in runners:
            self.add_runner(runner)

    def add_runner(self, runner):
        self.runners.append(runner)
        self.is_sorted = False

    def update_runner(self, runner):
        self.runners.remove(runner)

        self.add_runner(runner)

    def ranking_process(self):
        self.__filter_raw_ranking_by_runners()
        self.__set_points()

        self.is_sorted = True

    def disqualified_runner(self, current_runner):
        for runner in self.raw_ranking:
            if current_runner == runner:
                runner.is_disqualified = True

        self.is_sorted = False

    def get_ranking(self):
        if self.is_sorted is False:
            self.ranking_process()

        return self.ranking

    def __filter_raw_ranking_by_runners(self):
        self.ranking = [runner for runner in self.raw_ranking
                        if runner in self.runners
                            and runner.finished
                            and not runner.is_disqualified]

    def __set_points(self):
        # Asignar puntos como en la F1
        points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1, 0.75, 0.50, 0.25, 0.10, 0.05]
        point_index = 0

        for runner in self.ranking:
            if point_index <= len(points)-1:
                runner.points = points[point_index]

            runner.position = point_index + 1
            runner.posiciones_ant.append(runner.position)
            runner.averages_ant.append(runner.real_avg_time)
            runner.position_general_ant.append(runner.real_pos)

            point_index = point_index + 1
