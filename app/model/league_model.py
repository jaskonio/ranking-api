"""_summary_

Returns:
    _type_: _description_
"""
from collections import Counter
from datetime import timedelta
import logging
from typing import List
from pydantic import Field
from app.domain.UtilsRunner import convert_string_to_timedelta, convert_timedelta_to_string
from app.model.BaseMongoModel import BaseMongoModel
from app.model.RaceBaseModel import RaceBaseModel
from app.model.RunnerParticipantModel import RunnerParticipantModel
from app.model.race_model import RaceModel
from app.model.ranking_view_model import RankingViewModelBase
from app.model.runner_base_model import RunnerBaseModel
from app.model.runner_model import RunnerModel

logger = logging.getLogger(__name__)

class LeagueModel(BaseMongoModel):
    """_summary_

    Args:
        BaseMongoModel (_type_): _description_

    Returns:
        _type_: _description_
    """
    name: str
    races: List[RaceModel] = Field(default_factory=list)
    final_ranking: List[RankingViewModelBase] = Field(default_factory=list)
    runnerParticipants: List[RunnerParticipantModel] = Field(default_factory=list)

    def get_races(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return sorted(self.races, key=lambda race: (race.order))

    def add_runner(self, new_runner: RunnerBaseModel):
        """_summary_

        Args:
            new_runner (RunnerBaseModel): _description_
        """
        self.runnerParticipants.append(new_runner)

    def add_runners(self, new_runners:List[RunnerBaseModel]):
        """_summary_

        Args:
            new_runner (RunnerBaseModel): _description_
        """
        self.runnerParticipants.extend(new_runners)

    def add_race(self, new_race: RaceModel):
        """_summary_

        Args:
            new_race (RaceBaseModel): _description_
        """
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

    def add_races(self, new_races: List[RaceBaseModel]):
        """_summary_

        Args:
            new_race (RaceBaseModel): _description_
        """
        for race in new_races:
            self.add_race(race)

    def calculate_final_ranking(self):
        """_summary_
        """
        ranking_league = {}

        for race in self.get_races():
            runners = race.get_runners_with_points()
            for index, runner in enumerate(runners):
                if runner.name not in ranking_league:
                    ranking_league[runner.name] = RunnerModel(**runner.dict())
                else:
                    ranking_league[runner.name].puntos += runner.puntos

        final_ranking:List[RunnerModel] = sorted(ranking_league.values(),
                                    key=lambda runner: (runner.puntos),
                                    reverse=True)
        runner_final_ranking:List[RankingViewModelBase] = []

        for index, runner in enumerate(final_ranking):
            new_runner = RankingViewModelBase()
            new_runner.position = index+1
            new_runner.photo = runner.photo
            new_runner.points = runner.puntos
            new_runner.name = runner.name + runner.last_name

            if len(runner.posiciones_ant) != 0:
                new_runner.pos_last_race = runner.posiciones_ant[-1]
                new_runner.top_five = len([x for x in runner.posiciones_ant if x<=5])

                new_runner.participations = len(runner.posiciones_ant)
                new_runner.best_position = str(min(runner.posiciones_ant)) + '(x' + str(Counter(runner.posiciones_ant)[min(runner.posiciones_ant)]) + ')'
                new_runner.last_position_race = runner.poistion_general_ant[-1]
                new_runner.best_avegare_peace = self.__get_best_avegare_peace(runner.averages_ant, "mm:ss / km")
            #new_runner.best_position_real = runner.photo

            runner_final_ranking.append(new_runner)

        self.final_ranking = runner_final_ranking

    def disqualify_runner_process(self, bib_number:int, race_name:str):
        """_summary_

        Args:
            bib_number (int): _description_
            race_name (str): _description_
        """
        disqualified_runner = self.__get_runner_by_bib_number(bib_number)
        if not disqualified_runner:
            return
        current_race = self.__get_race_by_name(race_name)
        self.__disqualify_runner(disqualified_runner, current_race)
        self.__update_subsequent_races(disqualified_runner, current_race)

    def __get_disqualified_runners(self):
        disqualified_runners: List[RunnerBaseModel] = []

        for race in self.get_races():
            disqualified_runners.extend(race.runnerDisqualified)

        return disqualified_runners

    # def __other_criteria_ordenation(self, runner):
    #     try:
    #         return sum(runner.posiciones_ant) / len(runner.posiciones_ant)
    #     except:
    #         return 0

    def __filter_participants(self, race: RaceModel):
        if len(self.runnerParticipants) == 0:
            logging.warn("There are no participants in the League")

        runner_participants_in_race:List[RunnerModel] = []

        for runner in race.ranking:
            for participant in self.runnerParticipants:
                if runner.dorsal == participant.dorsal:
                    runner.photo = participant.photo
                    runner_participants_in_race.append(runner)
                elif runner.name == participant.name + ' ' + participant.last_name:
                    runner.photo = participant.photo
                    runner_participants_in_race.append(runner)

        return runner_participants_in_race

    def __get_runner_by_bib_number(self, bib_number:int):
        return next((runner for runner in self.runnerParticipants if runner.dorsal == bib_number), None)

    def __get_race_by_name(self, race_name: str):
        return next((race for race in self.races if race.name == race_name), None)

    def __disqualify_runner(self, runner:RunnerBaseModel, current_race:RaceModel):
        current_race.set_runner_disqualified(runner)

    def __update_subsequent_races(self, disqualified_runner: RunnerBaseModel, current_race: RaceModel):
        subsequent_races = [race for race in self.get_races() if race.order > current_race.order]
        for race in subsequent_races:
            race.set_runner_disqualified(disqualified_runner)

    def __get_previus_runner(self, current_runner: RunnerModel):
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
