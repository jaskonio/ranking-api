import logging
from collections import Counter
from datetime import timedelta
from typing import List
from app.core.mapper_utils import dicts_to_class
from app.domain.model.base_entity import BaseEntity
from app.domain.model.race import Race
from app.domain.model.runner import Runner
from app.domain.model.runner_league_ranking import RunnerLeagueRanking
from app.domain.services.UtilsRunner import convert_string_to_timedelta, convert_timedelta_to_string


logger = logging.getLogger(__name__)

class League(BaseEntity):
    def __init__(self, id:str='0', name:str='', races: List[Race] = None, ranking:List[RunnerLeagueRanking] = None
                 , runners: List[Runner] = None ):
        self.id = str(id)
        self.name = name
        self.races:List[Race] = dicts_to_class(Race, races)
        self.ranking:List[RunnerLeagueRanking] = dicts_to_class(RunnerLeagueRanking, ranking)
        self.runners:List[Runner] = dicts_to_class(Runner, runners)

    def add_runners(self, new_runners:List[Runner]):
        for new_runner in new_runners:
            self.add_runner(new_runner)

    def add_runner(self, new_runner: Runner):
        self.runners.append(new_runner)

    def delete_runners(self, runners:List[Runner]):
        for runner in runners:
            self.delete_runner(runner)

    def delete_runner(self, runner: Runner):
        if runner in self.runners:
            self.runners.remove(runner)

    def add_races(self, new_races: List[Race]):
        for race in new_races:
            self.add_race(race)

    def add_race(self, new_race: Race):
        new_race.participants = self.runners
        runners_disqualified = self.__get_all_previus_disqualified_runners()
        for runner in runners_disqualified:
            new_race.disqualified_runner(runner)

        new_race.ranking_process()

        for current_runner in new_race.get_ranking():
            previus_runner = self.__get_previus_runner(current_runner)

            if previus_runner is None:
                continue

            current_runner.posiciones_ant = previus_runner.posiciones_ant
            current_runner.posiciones_ant.append(current_runner.position)

            current_runner.averages_ant = previus_runner.averages_ant
            current_runner.averages_ant.append(current_runner.real_avg_time)

            current_runner.position_general_ant = previus_runner.position_general_ant
            current_runner.position_general_ant.append(current_runner.real_pos)

        self.races.append(new_race)
        self.calculate_final_ranking()

    def get_races(self):
        return sorted(self.races, key=lambda race: (race.order))

    def calculate_final_ranking(self):
        ranking_league = {}

        for race in self.get_races():
            runners = race.get_ranking()

            for runner in runners:
                if runner.id not in ranking_league:
                    ranking_league[runner.id] = runner
                else:
                    ranking_league[runner.id].points += runner.points

        final_ranking:List[RunnerLeagueRanking] = sorted(ranking_league.values(),
                                    key=lambda runner: (runner.points),
                                    reverse=True)

        runner_final_ranking:List[RunnerLeagueRanking] = []

        for index, runner in enumerate(final_ranking):
            new_runner = RunnerLeagueRanking(id=runner.id, first_name=runner.first_name, last_name=runner.last_name,
                                             photo=runner.photo, photo_url=runner.photo_url)
            new_runner.position = index + 1

            if len(runner.posiciones_ant) != 0:
                new_runner.pos_last_race = runner.posiciones_ant[-1]
                new_runner.top_five = len([x for x in runner.posiciones_ant if x<=5])

                new_runner.participations = len(runner.posiciones_ant)
                new_runner.best_position = str(min(runner.posiciones_ant)) \
                    + '(x' + str(Counter(runner.posiciones_ant)[min(runner.posiciones_ant)]) + ')'
                new_runner.last_position_race = runner.position_general_ant[-1]
                new_runner.best_avegare_peace = self.__get_best_avegare_peace(
                    runner.averages_ant, "mm:ss / km")

            runner_final_ranking.append(new_runner)

        self.ranking = runner_final_ranking

    def disqualify_runner_process(self, runner_id:int, race_name:str):
        disqualified_runner = [runner for runner in self.runners if runner.id == runner_id]

        if len(disqualified_runner) == 0:
            return None

        current_race = [race for race in self.races if race.name == race_name][0]

        current_race.disqualified_runner(disqualified_runner)
        self.__update_subsequent_races(disqualified_runner, current_race)

    def __get_all_previus_disqualified_runners(self):
        disqualified_runners: List[Runner] = []

        for race in self.get_races():
            race_disqualified_runners = [runner for runner in race.get_ranking() if runner.is_disqualified]
            disqualified_runners.extend(race_disqualified_runners)

        return disqualified_runners

    def __update_subsequent_races(self, disqualified_runner: Runner, current_race: Race):
        subsequent_races = [race for race in self.get_races() if race.order > current_race.order]
        for race in subsequent_races:
            race.disqualified_runner(disqualified_runner)

    def __get_previus_runner(self, current_runner: RunnerLeagueRanking):
        previus_race = self.__get_previus_race()

        if previus_race is None:
            return None

        for runner in previus_race.ranking:
            if runner == current_runner:
                return runner

        return None

    def __get_previus_race(self):
        if len(self.races) == 0:
            return None

        return self.races[-1]

    def __get_best_avegare_peace(self, averages:List[str], format_type):
        average_times:List[timedelta] = []

        for average_string in averages:
            average_time = convert_string_to_timedelta(average_string, format_type)
            average_times.append(average_time)

        min_average_time = min(average_times)

        return convert_timedelta_to_string(min_average_time, format_type)
