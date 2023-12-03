import unittest
from app.domain.model.runner_race_ranking import RunnerRaceRanking
from app.domain.services.sportmaniacs_mapper_service import SportmaniacsMapperService


class TestSportmaniacsMapperService(unittest.TestCase):
    def setUp(self):
        self.mapper_service = SportmaniacsMapperService()

    def test_return_0_when_when_runner_contain_only_name_field(self):
        data = {
            'data': {
                'Rankings': [
                    {'name': 'runner_1'},
                    {'name': 'runner_2'},
                    {'name': 'runner_3'},
                ]
            }
        }

        result = self.mapper_service.execute(data)

        expected_result = []

        self.assertEqual(result, expected_result)


    def test_return_rows_when_filtered_by_team_name(self):
        data = {
            'data': {
                'Rankings': [
                    {'club': 'Redolat'},
                    {'club': 'other_team'},
                    {'club': 'redolat team'},
                ]
            }
        }

        result = self.mapper_service.execute(data)
        expected_result = [RunnerRaceRanking(club='Redolat'),
            RunnerRaceRanking('redolat team'),
        ]

        for index in range(len(result)-1):
            self.assertEqual(result[index], expected_result[index])

    def test_execute_return_empty_list_when_data_not_contain_keys(self):
        data = {
            'data': {                
            }
        }

        result = self.mapper_service.execute(data)
        self.assertEqual(result, [])

        data = {}
        result = self.mapper_service.execute(data)
        self.assertEqual(result, [])

    def test_convert_to_gender(self):
        data = {
            'data': {
                'Rankings': [
                    {'name': 'runner_1', 'club': 'Redolat', 'gender': ''},
                    {'name': 'runner_3', 'club': 'Redolat', 'gender': None},
                    {'name': 'runner_2', 'club': 'Redolat', 'gender': 'gender_0'},
                    {'name': 'runner_3', 'club': 'Redolat', 'gender': 'gender_1'},
                ]
            }
        }

        result = self.mapper_service.execute(data)

        expected_result = [
            RunnerRaceRanking(first_name='runner_1', club='Redolat', gender=''),
            RunnerRaceRanking(first_name='runner_1', club='Redolat', gender=None),
            RunnerRaceRanking(first_name='runner_1', club='Redolat', gender='Masculino'),
            RunnerRaceRanking(first_name='runner_1', club='Redolat', gender='Femenino'),
        ]

        expected_result = []

        for index in range(len(result)-1):
            self.assertEqual(result[index], expected_result[index])
