import logging
import re
import requests
from typing import List
from app.domain.model.race_data_model import RunnerRaceDataModel
from app.domain.model.race_info_model import RaceModel
from app.domain.repository.idownloader_service import IDownloaderService
from app.domain.services.UtilsRunner import strtobool


class SportmaniacsDownloaderV1Service(IDownloaderService):
    def __init__(self, race_info:RaceModel, club_names:List[str]):
        self.logger = logging.getLogger(__name__)
        self.race_info = race_info
        self.club_names = club_names

    def get_data(self):
        try:
            reponse_json = self.__request(self.race_info)

            if 'data' not in reponse_json:
                return []

            if 'Rankings' not in reponse_json['data']:
                return []
            
            race_data:List[RunnerRaceDataModel] = self.__build_runners_model(reponse_json['data']['Rankings'])
            return race_data
        except Exception as exception_error:
            self.logger.error("Error process request: ", exception_error)
            raise TypeError(f'SportmaniacsDownloaderV1Service no supported url: {self.race_info.url}')

    def __request(self, race_info:RaceModel):
        race_id = 'None'

        pattern = r'([a-f0-9-]{36})'
        match = re.search(pattern, race_info.url)
        if match:
            race_id = match.group(0)

        url = 'https://sportmaniacs.com/es/races/rankings/' + race_id
        response = requests.get(url, timeout=60)
        response_json = response.json()
        return response_json

    def __build_runners_model(self, runners) -> List[RunnerRaceDataModel]:
        new_runners = []

        for row in runners:
            if "club" not in row:
                continue

            if row["club"].lower() not in self.club_names:
                continue

            runner = self.__build_runner_model(row)
            new_runners.append(runner)

        return new_runners

    def __build_runner_model(self, row) -> RunnerRaceDataModel:
        runner = RunnerRaceDataModel()
        runner.first_name = " ".join(row["name"].split()) if "name" in row else None
        runner.last_name = ""
        runner.gender = self.__convert_to_gender(row["gender"]) if "gender" in row else None
        runner.dorsal = row["dorsal"] if "dorsal" in row else None
        runner.category = row["category"] if "category" in row else None
        runner.club = row["club"] if "club" in row else None
        # runner.nationality = row["nationality"] if "nationality" in row else None
        runner.finished = strtobool(row["finishedRace"]) if "finishedRace" in row else None

        if "pos" in row:
            if row["pos"] != '':
                runner.official_pos = int(row["pos"])

        runner.official_time = row["officialTime"] if "officialTime" in row else None
        runner.official_avg_time = row["average"] if "average" in row else None

        if "catPos" in row:
            if row["catPos"] != '':
                runner.official_cat_pos = int(row["catPos"])

        if "genPos" in row:
            if row["genPos"] != '':
                runner.official_gen_pos = int(row["genPos"])


        runner.real_time = row["realTime"] if "realTime" in row else None
        runner.real_avg_time = row["averageNet"] if "averageNet" in row else None

        if "realPos" in row:
            if row["realPos"] != '':
                runner.real_pos = int(row["realPos"])

        if "realCatPos" in row:
            if row["realCatPos"] != '':
                runner.real_cat_pos = int(row["realCatPos"])

        if "realGenPos" in row:
            if row["realGenPos"] != '':
                runner.real_gen_pos = int(row["realGenPos"])

        return runner

    def __convert_to_gender(self, gender_string) -> str:
        if gender_string == '' or gender_string is None:
            return None

        gender_value = ''

        if gender_string == 'gender_0':
            gender_value = 'H'
        else:
            gender_value = 'M'

        return gender_value
