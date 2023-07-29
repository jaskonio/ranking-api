from app.aplication.downloader import Downloader
from app.aplication.UtilsRunner import strtobool
from app.domain.model.runner_race_detail import RunnerRaceDetail


class Sportmaniacs(Downloader):
    url_base = 'https://sportmaniacs.com/es/races/rankings/'

    def __init__(self, url):
        super().__init__(url)

    def process_url(self):
        url_race = self.url
        self.race_id = url_race.split('/')[-1]
        self.race_name = url_race.split('/')[5:6][0]
        self.requests_options['url'] = self.url_base + self.race_id

    def process_data(self):
        json_response_data = self.requests_response.json()
        data_filtered_by_club = self.__get_rankings_by_club(json_response_data)
        self.race_data = self.__set_rankings_format(data_filtered_by_club)

    def __get_rankings_by_club(self, json_response_data):
        rankings = json_response_data['data']['Rankings']

        rankings_by_club_list = []
        for row in rankings:
            if row['club'].lower() in self.team_name:
                rankings_by_club_list.append(row)

        return rankings_by_club_list

    def __set_rankings_format(self, runners):
        delete_keys = ['category_id', 'user_id', 'defaultImage', 'photos',
                       'externalPhotos', 'externalVideos', 'externalDiploma', 'Points']

        new_runners = []

        for row in runners:
            # delete key pos
            key_pos = [key for key in row.keys() if 'pos_' in key][0]
            delete_keys.append(key_pos)
            # delete keys
            [row.pop(key, None) for key in delete_keys]

            # Update gender value
            row['gender'] = 'Masculino' if row['gender'] == 'gender_0' else 'Femenino'

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
        runner.gender = row["gender"]
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
