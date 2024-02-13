from typing import List
from app.domain.repository.imappers_service import IMapperService
from app.domain.services.UtilsRunner import strtobool
from app.domain.model.runner_race_ranking import RunnerRaceRanking

class SportmaniacsMapperService(IMapperService):
    # base_url = 'https://sportmaniacs.com/es/races/rankings/'

    def __init__(self):
        pass

    def execute(self, data:any):
        if 'data' not in data:
            return []

        if 'Rankings' not in data['data']:
            return []

        race_data:List[RunnerRaceRanking] = self.__build_runners_model(data['data']['Rankings'])

        return race_data

    def __build_runners_model(self, runners):
        new_runners = []

        for row in runners:
            runner = self.__build_runner_model(row)

            new_runners.append(runner)

        return new_runners

    def __build_runner_model(self, row):
        runner = RunnerRaceRanking()
        runner.first_name = " ".join(row["name"].split()) if "name" in row else None
        runner.dorsal = row["dorsal"] if "dorsal" in row else None
        runner.club = row["club"] if "club" in row else None
        runner.nationality = row["nationality"] if "nationality" in row else None
        runner.finished = strtobool(row["finishedRace"]) if "finishedRace" in row else None
        runner.gender = self.__convert_to_gender(row["gender"]) if "gender" in row else None
        runner.category = row["category"] if "category" in row else None

        if "pos" in row:
            if row["pos"] != '':
                runner.position = int(row["pos"])

        runner.official_time = row["officialTime"] if "officialTime" in row else None
        runner.official_avg_time = row["average"] if "average" in row else None

        if "pos" in row:
            if row["pos"] != '':
                runner.official_pos = int(row["pos"])

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

    def __convert_to_gender(self, gender_string):
        if gender_string == '' or gender_string is None:
            return None

        gender_value = ''

        if gender_string == 'gender_0':
            gender_value = 'Masculino'
        else:
            gender_value = 'Femenino'

        return gender_value
