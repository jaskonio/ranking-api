import copy
import unittest
from tests.utils.league_builder import LeagueBuilder
from tests.utils.race_builder import RaceBuilder

from tests.utils.race_utils import build_races
from tests.utils.runner_race_ranking_utils import build_runners_race_ranking
from tests.utils.runner_utils import build_runner, build_runners


class TestLeague(unittest.TestCase):
    def test_add_runner(self):
        # Setup
        league_fake = LeagueBuilder().build()
        expected_runner_fake = build_runner()

        # Act
        league_fake.add_runner(copy.deepcopy(expected_runner_fake))
        runners = league_fake.participants

        # Assert
        self.assertEqual(runners, [expected_runner_fake])

    def test_add_runners(self):
        # Setup
        league_fake = LeagueBuilder().build()
        expected_runner_fake = build_runners(2)

        # Act
        league_fake.add_runners(copy.deepcopy(expected_runner_fake))
        runners = league_fake.participants

        # Assert
        self.assertEqual(runners, expected_runner_fake)

    def test_delete_runner(self):
        # Setup
        league_fake = LeagueBuilder().build()
        expected_runner_fake = build_runners(2)

        # Act
        league_fake.add_runners(copy.deepcopy(expected_runner_fake))
        league_fake.delete_runner(expected_runner_fake[0])

        runners = league_fake.participants

        # Assert
        self.assertEqual(len(runners), 1)
        self.assertEqual(runners, [expected_runner_fake[1]])

    def test_delete_runners(self):
        # Setup
        league_fake = LeagueBuilder().build()
        expected_runner_fake = build_runners(2)

        # Act
        league_fake.add_runners(copy.deepcopy(expected_runner_fake))
        league_fake.delete_runners(expected_runner_fake)

        runners = league_fake.participants

        # Assert
        self.assertEqual(len(runners), 0)

    def test_delete_runners_when_contains_3_runners(self):
        # Setup
        league_fake = LeagueBuilder().build()
        expected_runner_fake = build_runners(3)

        # Act
        league_fake.add_runners(copy.deepcopy(expected_runner_fake))
        league_fake.delete_runners([expected_runner_fake[0]])

        runners = league_fake.participants

        # Assert
        self.assertEqual(len(runners), 2)
        self.assertEqual(runners, [expected_runner_fake[1], expected_runner_fake[2]])

    def test_delete_runners_when_no_contain_runners(self):
        # Setup
        league_fake = LeagueBuilder().build()
        expected_runner_fake = build_runner()

        # Act
        league_fake.delete_runners([expected_runner_fake])

        runners = league_fake.participants

        # Assert
        self.assertEqual(len(runners), 0)

    def test_get_races(self):
        # Setup
        league_fake = LeagueBuilder().build()
        race_fake = RaceBuilder().build()

        # Act
        league_fake.add_race(race_fake)
        races = league_fake.get_races()

        # Assert
        self.assertEqual(len(races), 1)
        self.assertEqual(races[0].order, 0)
