from typing import List
from app.domain.repository.imappers_service import IMapperService
from app.domain.services.UtilsRunner import strtobool
from app.domain.model.runner_race_detail import RunnerRaceDetail

class SportmaniacsMapperService(IMapperService):
    team_name = ['Redolat', 'redolatteam', 'redolat team']
    # base_url = 'https://sportmaniacs.com/es/races/rankings/'

    def __init__(self):
        pass

    def execute(self, data:any):
        data_filtered_by_club = self.__filter_by_team_name(data['data']['Rankings'])
        race_data:List[RunnerRaceDetail] = self.__build_runners_model(data_filtered_by_club)

        return race_data

    def __filter_by_team_name(self, rankings):
        rankings_by_club_list = []
        for row in rankings:
            if row['club'].lower() in self.team_name:
                rankings_by_club_list.append(row)

        return rankings_by_club_list

    def __build_runners_model(self, runners):
        new_runners = []

        for row in runners:
            runner = self.__build_runner_model(row)

            new_runners.append(runner)

        return new_runners

    def __build_runner_model(self, row):
        runner = RunnerRaceDetail()
        runner.first_name = row["name"]
        runner.dorsal = row["dorsal"]
        runner.club = row["club"]
        runner.nationality = row["nationality"]
        runner.finished = strtobool(row["finishedRace"])
        runner.gender = 'Masculino' if row["gender"] == 'gender_0' else 'Femenino'
        runner.category = row["category"]
        runner.position = row["pos"]

        runner.official_time = row["officialTime"]
        runner.official_avg_time = row["average"]
        runner.official_cat_pos = row["catPos"]
        runner.official_gen_pos = row["genPos"]

        runner.real_time = row["realTime"]
        runner.real_avg_time = row["averageNet"]
        runner.real_pos = row["realPos"]
        runner.real_cat_pos = row["realCatPos"]
        runner.real_gen_pos = row["realGenPos"]

        return runner