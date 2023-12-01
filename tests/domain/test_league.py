import copy
import unittest

from tests.utils.league_utils import build_league
from tests.utils.race_utils import build_race, build_races
from tests.utils.runner_race_ranking_utils import build_runners_race_ranking
from tests.utils.runner_utils import build_runner, build_runners


class TestLeague(unittest.TestCase):
    def test_add_runner(self):
        # Setup
        league_fake = build_league()
        expected_runner_fake = build_runner()

        # Act
        league_fake.add_runner(copy.deepcopy(expected_runner_fake))
        runners = league_fake.participants

        # Assert
        self.assertEqual(runners, [expected_runner_fake])

    def test_add_runners(self):
        # Setup
        league_fake = build_league()
        expected_runner_fake = build_runners(2)

        # Act
        league_fake.add_runners(copy.deepcopy(expected_runner_fake))
        runners = league_fake.participants

        # Assert
        self.assertEqual(runners, expected_runner_fake)

    def test_delete_runner(self):
        # Setup
        league_fake = build_league()
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
        league_fake = build_league()
        expected_runner_fake = build_runners(2)

        # Act
        league_fake.add_runners(copy.deepcopy(expected_runner_fake))
        league_fake.delete_runners(expected_runner_fake)

        runners = league_fake.participants

        # Assert
        self.assertEqual(len(runners), 0)

    def test_delete_runners_when_contains_3_runners(self):
        # Setup
        league_fake = build_league()
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
        league_fake = build_league()
        expected_runner_fake = build_runner()

        # Act
        league_fake.delete_runners([expected_runner_fake])

        runners = league_fake.participants

        # Assert
        self.assertEqual(len(runners), 0)

    def test_get_races(self):
        # Setup
        league_fake = build_league()
        raw_ranking_fake = build_runners_race_ranking(3)
        runners_fake = build_runners(3)
        race_fake = build_race(runners_fake=runners_fake, raw_ranking_fake=raw_ranking_fake)

        # Act
        league_fake.add_race(race_fake)
        races = league_fake.get_races()

        # Assert
        self.assertEqual(len(races), 1)
        self.assertEqual(races[0].order, 0)

    def test_get_races_with_3_races(self):
        # Setup
        races_fake = build_races(3)
        league_fake = build_league(races=copy.deepcopy(races_fake))

        # Act
        races = league_fake.get_races()

        # Assert
        self.assertEqual(len(races), len(races_fake))
        for (race, expected_race) in zip(races, races_fake):
            self.assertEqual(race.order, expected_race.order)

    def test_get_races_when_set_races_desordenado(self):
        # Setup
        races_fake = build_races(3)
        expected_races_fake = copy.deepcopy(races_fake)

        league_fake = build_league()

        # Act
        league_fake.add_race(expected_races_fake[2])
        league_fake.add_race(expected_races_fake[0])
        league_fake.add_race(expected_races_fake[1])
        races = league_fake.get_races()

        # Assert
        self.assertEqual(len(races), len(races_fake))
        for (race, expected_race) in zip(races, races_fake):
            self.assertEqual(race.order, expected_race.order)

    def test_add_race_when_no_contain_runner_league(self):
        # Setup
        race_fake = build_race()
        expected_race_fake = copy.deepcopy(race_fake)

        league_fake = build_league()

        # Act
        league_fake.add_race(expected_race_fake)
        races = league_fake.get_races()

        # Assert
        self.assertEqual(len(races), 1)
        self.assertEqual(len(races[0].participants), 0)
        self.assertEqual(len(races[0].ranking), 0)
        self.assertEqual(len(league_fake.ranking), 0)
        self.assertEqual(len(league_fake.participants), 0)

    def test_add_race_when_contain_runner_league_and_whiuout_raw_runners(self):
        # Setup
        race_fake = build_race()
        expected_race_fake = copy.deepcopy(race_fake)

        runners_fake = build_runners(3)
        expected_runners_fake = copy.deepcopy(runners_fake)
        league_fake = build_league(runners=expected_runners_fake)

        # Act
        league_fake.add_race(expected_race_fake)
        races = league_fake.get_races()

        # Assert
        self.assertEqual(len(races), 1)
        self.assertEqual(len(races[0].raw_ranking), 0)
        self.assertEqual(len(races[0].ranking), 0)
        self.assertEqual(len(races[0].participants), len(runners_fake))
        self.assertEqual(len(league_fake.ranking), 0)
        self.assertEqual(len(league_fake.participants), len(runners_fake))

    def test_add_race_when_3_raw_ranking_and_0_runner_league(self):
        # Setup
        raw_ranking_fake = build_runners_race_ranking(3)
        race_fake = build_race(raw_ranking_fake=raw_ranking_fake)
        expected_race_fake = copy.deepcopy(race_fake)

        league_fake = build_league()

        # Act
        league_fake.add_race(expected_race_fake)
        races = league_fake.get_races()

        # Assert
        self.assertEqual(len(races), 1)
        self.assertEqual(len(races[0].raw_ranking), len(raw_ranking_fake))
        self.assertEqual(len(races[0].ranking), 0)
        self.assertEqual(len(races[0].participants), 0)
        self.assertEqual(len(league_fake.ranking), 0)
        self.assertEqual(len(league_fake.participants), 0)
        