import logging
import re
import requests
from typing import List
from app.domain.model.race_data_model import RunnerRaceDataModel
from app.domain.model.race_info_model import RaceModel
from app.domain.repository.idownloader_service import IDownloaderService
from app.domain.services.UtilsRunner import average_to_format_string, time_seconds_to_string_format


class SportmaniacsDownloaderV2Service(IDownloaderService):
    def __init__(self, race_info:RaceModel, club_names:List[str]):
        self.logger = logging.getLogger(__name__)
        self.race_info = race_info
        self.club_names = club_names

    def get_data(self):
        runners = self.__get__all_runners(self.race_info)

        if len(runners) == 0:
            return []

        runners_filtered = self.__filter_runners_by_club(runners)
        runners_filtered = self.__filter_runners_by_finish(runners_filtered)
        race_data:List[RunnerRaceDataModel] = self.__build_runners_model(runners_filtered)

        race_data_sorted = sorted(race_data, key=lambda x: (x.finished==False, x.real_pos))
        return race_data_sorted

    def __get__all_runners(self, race_info:RaceModel):
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

    def __filter_runners_by_finish(self, runners: List[any]):
        runners_filtered = []
        for runner in runners:
            if 'status' not in runner:
                continue

            if runner['status'].lower() != 'finished':
                continue

            runners_filtered.append(runner)

        return runners_filtered

    def __build_runners_model(self, runners) -> List[RunnerRaceDataModel]:
        runners_models = []
        
        for runner in runners:
            runner_model = self.__build_runner_model(runner)
            if runner_model is not None:
                runners_models.append(runner_model)

        return  runners_models

    def __build_runner_model(self, row) -> RunnerRaceDataModel:
        runner = RunnerRaceDataModel()
        try:
            runner.first_name = row['name']
            runner.last_name = row['surname']
            # runner.nationality = '' if 'nationality' not in row else row["nationality"]
            runner.gender = self.__convert_to_gender(row["gender"])

            runner.dorsal = row["dorsal"]
            runner.category =  ''
            runner.club = row["club"]
            runner.finished = True if row["status"] == 'finished' else False

            if 'Meta' in row["rankings"] and row["rankings"]['Meta']['pos'] != 0:
                runner.official_pos = int(row["rankings"]['Meta']['posNet'])
                runner.official_time = time_seconds_to_string_format(row["rankings"]['Meta']['net'])
                runner.official_avg_time = average_to_format_string(row["rankings"]['Meta']['averageNet'])
                runner.official_cat_pos = int(row["rankings"]['Meta']['posCatNet'])
                runner.official_gen_pos = int(row["rankings"]['Meta']['posGenNet'])

                runner.real_pos = int(row["rankings"]['Meta']['pos'])
                runner.real_time = time_seconds_to_string_format(row["rankings"]['Meta']['time'])
                runner.real_avg_time = average_to_format_string(row["rankings"]['Meta']['average'])
                runner.real_cat_pos = int(row["rankings"]['Meta']['posCat'])
                runner.real_gen_pos = int(row["rankings"]['Meta']['posGen'])
    
            elif 'custom-rankings' in row:
                real_pos = 0
                real_cat_pos = 0
                real_gen_pos = 0
                if row["custom-rankings"][0]['pos'] != 0:
                    real_pos = row["custom-rankings"][0]['pos']
                else:
                    raise TypeError("No es posible generar el real_pos") 
                if row["custom-rankings"][1]['pos'] != 0:
                    real_cat_pos = row["custom-rankings"][1]['pos']
                else:
                    raise TypeError("No es posible generar el real_cat_pos") 
                if row["custom-rankings"][2]['pos'] != 0:
                    real_gen_pos = row["custom-rankings"][2]['pos']
                else:
                    raise TypeError("No es posible generar el real_gen_pos")

                runner.real_pos = int(real_pos)
                runner.real_cat_pos = int(real_cat_pos)
                runner.real_gen_pos = int(real_gen_pos)

            return runner

        except Exception as exception_error:
            self.logger.error(f'Error to build runner: {runner.full_name}')
            self.logger.error(exception_error)
            return None

    def __convert_to_gender(self, gender_string) -> str:
        if gender_string == '' or gender_string is None:
            return None

        gender_value = ''

        if gender_string == 'male':
            gender_value = 'H'
        else:
            gender_value = 'M'

        return gender_value
