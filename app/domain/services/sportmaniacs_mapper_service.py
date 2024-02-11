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
        runner.position = row["position"] if "position" in row else None

        runner.official_time = row["official_time"] if "official_time" in row else None
        runner.official_avg_time = row["official_avg_time"] if "official_avg_time" in row else None
        runner.official_cat_pos = row["official_cat_pos"] if "official_cat_pos" in row else None
        runner.official_gen_pos = row["official_gen_pos"] if "official_gen_pos" in row else None

        runner.real_time = row["real_time"] if "real_time" in row else None
        runner.real_avg_time = row["real_avg_time"] if "real_avg_time" in row else None
        runner.real_pos = row["real_pos"] if "real_pos" in row else None
        runner.real_cat_pos = row["real_cat_pos"] if "real_cat_pos" in row else None
        runner.real_gen_pos = row["real_gen_pos"] if "real_gen_pos" in row else None

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
