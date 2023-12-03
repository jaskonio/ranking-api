import copy
import unittest
from tests.utils.league_builder import LeagueBuilder
from tests.utils.race_builder import RaceBuilder
from tests.utils.runner_base_builder import RunnerBaseBuilder
from tests.utils.runner_race_ranking_builder import RunnerRaceRankingBuilder
from tests.utils.runner_race_ranking_utils import build_runners_race_ranking
from tests.utils.runner_utils import build_runners


class TestLeague(unittest.TestCase):
    def setUp(self):
        id_fake = "R001"
        name_fake = "R001"
        raw_ranking_fake = build_runners_race_ranking(16)
        new_race = RaceBuilder(id=id_fake, name=name_fake).with_raw_ranking(raw_ranking_fake).build()

        self.mock_race = new_race
        self.mock_participants = build_runners(1)

        self.mock_runner_league_ranking = RunnerRaceRankingBuilder().build()

    def test_add_runner(self):
        league = LeagueBuilder().with_participants(self.mock_participants).build()
        new_runner = RunnerBaseBuilder().build()
        league.add_runner(new_runner)
        self.assertIn(new_runner, league.participants)

    def test_delete_runner(self):
        mock_participants = build_runners(1)
        expected_mock_participants = copy.deepcopy(mock_participants)

        league = LeagueBuilder().with_participants(mock_participants).build()

        league.delete_runner(expected_mock_participants[0])

        self.assertNotIn(expected_mock_participants[0], league.participants)

    def test_add_race(self):
        # runners_fake = build_runners(16)
        league = LeagueBuilder().with_participants(self.mock_participants).build()

        id_fake = "R001"
        name_fake = "R001"
        raw_ranking_fake = build_runners_race_ranking(16)
        new_race = RaceBuilder(id=id_fake, name=name_fake).with_raw_ranking(raw_ranking_fake).build()

        league.add_race(new_race)
        self.assertIn(new_race, league.races)

    def test_calculate_final_ranking_without_participant(self):
        league = LeagueBuilder().with_races([self.mock_race]).build()
        league.calculate_final_ranking()
        self.assertEqual([], league.ranking)

    def test_disqualify_runner_process(self):
        first_name = 'name_01'
        last_name = 'last_name_01'
        participants =[RunnerBaseBuilder().with_name(first_name, last_name).build()]
        raw_ranking = [RunnerRaceRankingBuilder().with_name(first_name, last_name).build()]
        race = RaceBuilder().with_raw_ranking(raw_ranking).build()
        league = LeagueBuilder().with_participants(participants).with_races([race]).build()

        league.disqualify_runner_process(runner_id=1, race_name=race.name)
        self.assertTrue(league.races[0].raw_ranking[0].is_disqualified)

if __name__ == '__main__':
    unittest.main()
