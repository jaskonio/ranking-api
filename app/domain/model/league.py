import logging
from collections import Counter
from datetime import timedelta
from typing import List
from app.aplication.UtilsRunner import convert_string_to_timedelta, convert_timedelta_to_string
from app.core.mapper_utils import dicts_to_class
from app.domain.model.base_entity import BaseEntity
from app.domain.model.race import Race
from app.domain.model.runner import Runner
from app.domain.model.runner_league_ranking import RunnerLeagueRanking
from app.domain.model.runner_race_detail import RunnerRaceDetail


logger = logging.getLogger(__name__)

class League(BaseEntity):
    def __init__(self, id:str='0', name:str='', races: List[Race] = None, ranking:List[RunnerLeagueRanking] = None
                 , runners: List[Runner] = None ):
        self.id = str(id)
        self.name = name
        self.races:List[Race] = dicts_to_class(Race, races)
        self.ranking:List[RunnerLeagueRanking] = dicts_to_class(RunnerLeagueRanking, ranking)
        self.runners:List[Runner] = dicts_to_class(Runner, runners)

    def get_races(self):
        return sorted(self.races, key=lambda race: (race.order))

    def delete_runners(self, runners:List[Runner]):
        for runner in runners:
            self.delete_runner(runner)

    def delete_runner(self, current_runner: Runner):
        new_runners = [runner for runner in self.runners if runner != current_runner]
        self.runners = new_runners

    def add_runner(self, new_runner: Runner):
        self.runners.append(new_runner)

    def add_runners(self, new_runners:List[Runner]):
        self.runners.extend(new_runners)

    def add_race(self, new_race: Race):
        runners_participants_race = self.__filter_participants(new_race)
        new_race.set_runners_disqualified(self.__get_disqualified_runners())
        new_race.ranking = runners_participants_race

        new_race.set_points()

        # fill another properties
        # aqui iterar los runner para actulizar los valore acumulativos como 'posiciones_ant'
        #runners_populate: List[RunnerModel] = []

        for current_runner in new_race.ranking:
            previus_runner = self.__get_previus_runner(current_runner)

            if previus_runner is None:
                current_runner.posiciones_ant.append(current_runner.position)
                current_runner.averages_ant.append(current_runner.realAverageTime)
                current_runner.poistion_general_ant.append(current_runner.realPos)
                continue

            current_runner.posiciones_ant = previus_runner.posiciones_ant
            current_runner.posiciones_ant.append(current_runner.position)

            current_runner.averages_ant = previus_runner.averages_ant
            current_runner.averages_ant.append(current_runner.realAverageTime)

            current_runner.poistion_general_ant = previus_runner.poistion_general_ant
            current_runner.poistion_general_ant.append(current_runner.realPos)

        self.races.append(new_race)
        self.calculate_final_ranking()

    def add_races(self, new_races: List[Race]):
        for race in new_races:
            self.add_race(race)

    def calculate_final_ranking(self):
        ranking_league = {}

        for race in self.get_races():
            runners = race.get_runners_with_points()
            for index, runner in enumerate(runners):
                if runner.name not in ranking_league:
                    ranking_league[runner.name] = RunnerRaceDetail(**runner.dict())
                else:
                    ranking_league[runner.name].puntos += runner.puntos

        final_ranking:List[RunnerLeagueRanking] = sorted(ranking_league.values(),
                                    key=lambda runner: (runner.puntos),
                                    reverse=True)
        runner_final_ranking:List[RunnerLeagueRanking] = []

        for index, runner in enumerate(final_ranking):
            new_runner = RunnerLeagueRanking(runner.name, runner.last_name)
            new_runner.position = index+1
            new_runner.photo = runner.photo
            new_runner.points = runner.puntos
            #new_runner.name = runner.name + runner.last_name

            if len(runner.posiciones_ant) != 0:
                new_runner.pos_last_race = runner.posiciones_ant[-1]
                new_runner.top_five = len([x for x in runner.posiciones_ant if x<=5])

                new_runner.participations = len(runner.posiciones_ant)
                new_runner.best_position = str(min(runner.posiciones_ant)) \
                    + '(x' + str(Counter(runner.posiciones_ant)[min(runner.posiciones_ant)]) + ')'
                new_runner.last_position_race = runner.poistion_general_ant[-1]
                new_runner.best_avegare_peace = self.__get_best_avegare_peace(
                    runner.averages_ant, "mm:ss / km")

            runner_final_ranking.append(new_runner)

        self.ranking = runner_final_ranking

    def disqualify_runner_process(self, bib_number:int, race_name:str):
        disqualified_runner = self.__get_runner_by_bib_number(bib_number)

        if not disqualified_runner:
            return None

        current_race = self.__get_race_by_name(race_name)
        self.__disqualify_runner(disqualified_runner, current_race)
        self.__update_subsequent_races(disqualified_runner, current_race)

    def __get_disqualified_runners(self):
        disqualified_runners: List[Runner] = []

        for race in self.get_races():
            disqualified_runners.extend(race.runnerDisqualified)

        return disqualified_runners


    def __filter_participants(self, race: Race):
        if len(self.runners) == 0:
            logging.warn("There are no participants in the League")

        runner_participants_in_race:List[RunnerLeagueRanking] = []

        for runner in race.ranking:
            for participant in self.runners:
                if runner.dorsal == participant.dorsal or\
                runner.first_name == participant.first_name + ' ' + participant.last_name:
                    runner_participants_in_race.append(runner)

        return runner_participants_in_race

    def __get_runner_by_bib_number(self, bib_number:int):
        return next((runner for runner in self.runners if runner.dorsal == bib_number), None)

    def __get_race_by_name(self, race_name: str):
        return next((race for race in self.races if race.name == race_name), None)

    def __disqualify_runner(self, runner:Runner, current_race:Race):
        current_race.set_runner_disqualified(runner)

    def __update_subsequent_races(self, disqualified_runner: Runner, current_race: Race):
        subsequent_races = [race for race in self.get_races() if race.order > current_race.order]
        for race in subsequent_races:
            race.set_runner_disqualified(disqualified_runner)

    def __get_previus_runner(self, current_runner: RunnerLeagueRanking):
        previus_race = self.__get_previus_race()

        if previus_race is None:
            return None

        for runner in previus_race.ranking:
            if runner.dorsal == current_runner.dorsal or runner.name == current_runner.name:
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
