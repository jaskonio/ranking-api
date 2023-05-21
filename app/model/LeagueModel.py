from typing import List
from pydantic import Field
from .BaseMongoModel import BaseMongoModel
from .OID import OID
from .RaceModel import RaceModel
from .RunnerBaseModel import RunnerBaseModel
from .RunnerModel import RunnerModel

class LeagueModel(BaseMongoModel):
    id: OID = Field(default_factory=OID)
    name: str
    races: List[RaceModel] = Field(default_factory=list)
    finalRanking: List[RunnerModel] = Field(default_factory=list)
    runnerParticipants: List[RunnerBaseModel] = Field(default_factory=list)

    def get_races(self):
        return sorted(self.races, key=lambda race: (race.order))

    def add_runner(self, new_runner: RunnerBaseModel):
        self.runnerParticipants.append(new_runner)

    def add_race(self, new_race: RaceModel):
        runners_participants_race = self.__filter_participants(new_race)

        new_race.ranking = runners_participants_race
        new_race.set_runners_disqualified(self.__get_disqualified_runners())
        
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

    def disqualify_runner_process(self, bib_number:int, race_name:str):
        disqualified_runner = self.__get_runner_by_bib_number(bib_number)
        current_race = self.__get_race_by_name(race_name)
        self.__disqualify_runner(disqualified_runner, current_race)
        self.__update_subsequent_races(disqualified_runner, current_race)

    def __get_disqualified_runners(self):
        disqualified_runners: List[RunnerBaseModel] = []
        
        for race in self.get_races():
            disqualified_runners.extend(race.runnerDisqualified)
        
        return disqualified_runners
        
    def __order_runner(self, runner):
        try:
            return sum(runner.posiciones_ant) / len(runner.posiciones_ant)
        except :
            return 0

    def __filter_participants(self, race: RaceModel):
        bib_participants = [participant.dorsal for participant in self.runnerParticipants if participant.dorsal]
        return [runner for runner in race.ranking if runner.dorsal in bib_participants]

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
