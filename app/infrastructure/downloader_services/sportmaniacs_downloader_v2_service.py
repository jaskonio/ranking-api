import logging
import re
import requests
from typing import List
from app.domain.model.race_data_model import RunnerRaceDataModel
from app.domain.model.race_info_model import RaceInfoModel
from app.domain.repository.idownloader_service import IDownloaderService
from app.domain.services.UtilsRunner import average_to_format_string, time_seconds_to_string_format


class SportmaniacsDownloaderV2Service(IDownloaderService):
    def __init__(self, race_info:RaceInfoModel, club_names:List[str]):
        self.logger = logging.getLogger(__name__)
        self.race_info = race_info
        self.club_names = club_names

    def get_data(self):
        runners = self.__get__all_runners(self.race_info)

        if len(runners) == 0:
            return []

        runners_filtered = self.__filter_runners_by_club(runners)
        race_data:List[RunnerRaceDataModel] = self.__build_runners_model(runners_filtered)

        return race_data

    def __get__all_runners(self, race_info:RaceInfoModel):
        competition_id = self.__get_competition_id(race_info.url)
        
        url = f'https://rankings-storage.timingsense.cloud/prod/competitions/{competition_id}/Carrera%20(Modalidad%20competitiva)/participants.json'
        
        runners = requests.get(url, timeout=60).json()

        return runners

    def __get_competition_id(self, url):
        if '/rankings' not in url:
            url = url + '/rankings'

        html = requests.get(url, timeout=60).text
        regex = r'competitionId: "([a-f0-9-]+)"'
        matches = re.findall(regex, html)
        return matches[0]

    def __filter_runners_by_club(self, runners: List[any]):
        runners_filtered = []
        for runner in runners:
            if 'club' not in runner:
                continue
            if runner['club'].lower() not in self.club_names:
                continue
            runners_filtered.append(runner)

        return runners_filtered

    # def __filter_runners_by_persons_availables(self, runners: List[any]):
    #     runners_filtered = []

    #     for runner in runners:
    #         for person in self.persons:
    #             if runner['fullName'] == person.full_name:
    #                 runner['name'] = person.first_name
    #                 runner['surname'] = person.last_name
    #                 runner['photo_url'] = person.photo_url

    #                 runners_filtered.append(runner)

    #     return runners_filtered

    def __build_runners_model(self, runners) -> List[RunnerRaceDataModel]:
        return [self.__build_runner_model(runner) for runner in runners]

    def __build_runner_model(self, row) -> RunnerRaceDataModel:
        runner = RunnerRaceDataModel()
        try:
            runner.first_name = row['name']
            runner.last_name = row['surname']
            runner.nationality = '' if 'nationality' not in row else row["nationality"]
            runner.gender = self.__convert_to_gender(row["gender"])

            runner.dorsal = row["dorsal"]
            runner.category =  ''
            runner.club = row["club"]
            runner.finished = True if row["status"] == 'finished' else False

            if 'Meta' in row["rankings"]:
                runner.official_pos = int(row["rankings"]['Meta']['pos'])
                runner.official_time = time_seconds_to_string_format(row["rankings"]['Meta']['time'])
                runner.official_avg_time = average_to_format_string(row["rankings"]['Meta']['average'])
                runner.official_cat_pos = int(row["rankings"]['Meta']['posCat'])
                runner.official_gen_pos = int(row["rankings"]['Meta']['posGen'])

                runner.real_pos = int(row["rankings"]['Meta']['posNet'])
                runner.real_time = time_seconds_to_string_format(row["rankings"]['Meta']['net'])
                runner.real_avg_time = average_to_format_string(row["rankings"]['Meta']['averageNet'])
                runner.real_cat_pos = int(row["rankings"]['Meta']['posCatNet'])
                runner.real_gen_pos = int(row["rankings"]['Meta']['posGenNet'])

        except Exception as exception_error:
            self.logger.error(f'Error to build: {runner.first_name}')
            self.logger.error(exception_error)

        return runner

    def __convert_to_gender(self, gender_string) -> str:
        if gender_string == '' or gender_string is None:
            return None

        gender_value = ''

        if gender_string == 'male':
            gender_value = 'Masculino'
        else:
            gender_value = 'Femenino'

        return gender_value
