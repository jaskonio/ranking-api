from typing import List
from app.domain.downloader import Downloader
from app.domain.UtilsRunner import build_runner
from app.model.runner_model import RunnerModel

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
        delete_keys = ['category_id', 'user_id', 'defaultImage', 'photos', 'externalPhotos', 'externalVideos', 'externalDiploma', 'Points']
        
        new_runners:List[RunnerModel] = []
            
        for row in runners:
            # delete key pos
            key_pos = [key for key in row.keys() if 'pos_' in key][0]
            delete_keys.append(key_pos)
            # delete keys
            [row.pop(key, None) for key in delete_keys]

            # Update gender value
            row['gender'] = 'Masculino' if row['gender'] == 'gender_0' else 'Femenino'

            runner = build_runner(row["dorsal"], row["name"], row["club"], row["nationality"], row["finishedRace"], row["gender"], row["category"],
                                  row["officialTime"], row["pos"], row["average"], row["catPos"], row["genPos"],
                                  row["realTime"], row["realPos"], row["averageNet"], row["realCatPos"], row["realGenPos"])

            new_runners.append(runner)

        return new_runners
