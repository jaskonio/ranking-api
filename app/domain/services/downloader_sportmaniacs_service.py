from typing import List
from app.domain.model.person import Person
from app.domain.repository.idownloader_race_data import IDownloaderRaceData, IDownloaderServiceHTTPOption
from app.domain.repository.idownloader_service import IDownloaderService
from app.domain.repository.igeneric_repository import IGenericRepository
from app.domain.services.UtilsRunner import strtobool
from app.domain.model.runner_race_detail import RunnerRaceDetail


class DownloaderSportmaniacsService(IDownloaderService):
    team_name = ['Redolat', 'redolatteam', 'redolat team']
    base_url = 'https://sportmaniacs.com/es/races/rankings/'
    def __init__(self, race_repository: IDownloaderRaceData, person_repository: IGenericRepository):
        self.race_repository = race_repository
        self.person_repository = person_repository

    def get_data(self, url:str):
        options: IDownloaderServiceHTTPOption = IDownloaderServiceHTTPOption()
        options.method = 'GET'
        options.url = self.base_url + url.split('/')[-1]
        options.data = ''
        options.timeout = 60

        json_response_data = self.race_repository.get_data(options)
        data_filtered_by_club = self.__filter_by_team_name(json_response_data.json()['data']['Rankings'])
        race_data:List[RunnerRaceDetail] = self.__build_runners_model(data_filtered_by_club)
        race_data:List[RunnerRaceDetail] = self.__fill_person_properties(race_data)

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

    def __fill_person_properties(self, runners: List[RunnerRaceDetail]):
        persons: List[Person] = self.person_repository.get_all()
        runners_fill: List[RunnerRaceDetail] = []

        for runner in runners:
            for person in persons:
                if person.first_name + ' ' + person.last_name == runner.first_name:
                    runner.id = person.id
                    runner.first_name = person.first_name
                    runner.last_name = person.last_name
                    runner.nationality = person.nationality
                    runner.gender = person.gender
                    runner.photo = person.photo
                    runner.photo_url = person.photo_url
                    break

            runners_fill.append(runner)

        return runners_fill
