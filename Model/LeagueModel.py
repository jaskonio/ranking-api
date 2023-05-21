from typing import List
from pydantic import Field
from Model.BaseMongoModel import BaseMongoModel
from Model.OID import OID
from Model.RaceModel import RaceModel
from Model.RunnerBaseModel import RunnerBaseModel
from Model.RunnerModel import RunnerModel

class LeagueModel(BaseMongoModel):
    id: OID = Field(default_factory=OID)
    name: str
    races: List[RaceModel] = Field(default_factory=list)
    finalRanking: List[RunnerModel] = Field(default_factory=list)
    runnerParticipants: List[RunnerBaseModel] = Field(default_factory=list)

    def get_races(self):
        return sorted(self.races, key=lambda race: (race.order))

    def add_race(self, new_race: RaceModel):
        new_race.runnerDisqualified = self.__get_disqualified_runners()
        
        runners_participants_race = []
        bib_participants = [participant for participant in self.runnerParticipants if participant.dorsal]
        
        for runner in new_race.ranking:
            if runner.dorsal in bib_participants:
                runners_participants_race.append(runner)

        new_race.ranking = runners_participants_race

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
        runner = [runner for runner in self.runnerParticipants if runner.dorsal == bib_number][0]
        current_race = [race for race in self.races if race.name == race_name][0]

        self.disqualify_runner(runner, current_race)

        # el runner descalificado actualiza las siguientes carreras que existen
        for race in self.get_races():
            if current_race.order < race.order:
                race.set_runner_disqualified(runner)

    def disqualify_runner(self, runner:RunnerBaseModel, current_race:RaceModel):
        current_race = {}
        
        for race in self.races:
            if race.name == current_race.name:
                race.set_runner_disqualified(runner)

    def __get_disqualified_runners(self):
        disqualified_runners = []
        
        for race in self.get_races():
            disqualified_runners.extend(race.runnerDisqualified)
        
        return disqualified_runners

    def __order_runner(self, runner):
        try:
            return sum(runner.posiciones_ant) / len(runner.posiciones_ant)
        except :
            return 0

