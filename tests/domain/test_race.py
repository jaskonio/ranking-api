import copy
import unittest
from tests.utils.race_utils import build_race
from tests.utils.runner_race_ranking_utils import build_runner_race_ranking, build_runners_race_ranking
from tests.utils.runner_utils import build_runner, build_runners

class TestRace(unittest.TestCase):

    def test_set_raw_ranking(self):
        # Setup
        id_fake = "R001"
        name_fake = "R001"
        raw_ranking_fake = build_runners_race_ranking(3)
        race = build_race(id=id_fake, name=name_fake)

        # Assert
        self.assertEqual(len(race.get_raw_ranking()), 0)

        race.set_raw_ranking(raw_ranking_fake)

        self.assertEqual(len(race.get_raw_ranking()), len(raw_ranking_fake))

    def test_add_runner(self):
        # Setup
        id_fake = "R001"
        name_fake = "R001"
        runner_fake = build_runner()
        race = build_race(id=id_fake, name=name_fake)

        race.add_runner(runner_fake)

        # Assert
        self.assertEqual(race.is_sorted, False)

        self.assertEqual(len(race.runners), 1)
        self.assertEqual(race.runners[0], runner_fake)

    def test_add_runners(self):
        # Setup
        id_fake = "R001"
        name_fake = "R001"
        runners_fake = build_runners(3)
        race = build_race(id=id_fake, name=name_fake)

        race.add_runners(runners_fake)

        # Assert
        self.assertEqual(race.is_sorted, False)

        self.assertEqual(len(race.runners), len(runners_fake))
        self.assertEqual(race.runners, runners_fake)

    def test_update_runner(self):
        # Setup
        id_fake = "R001"
        name_fake = "R001"
        runners_fake = build_runners(2)
        race = build_race(id=id_fake, name=name_fake, runners_fake=runners_fake)

        expected_runners = copy.deepcopy(runners_fake)
        expected_runners[1].last_name = "new_name"

        race.update_runner(expected_runners[1])

        # Assert
        self.assertEqual(race.is_sorted, False)

        self.assertEqual(len(race.runners), len(expected_runners))
        self.assertEqual(race.runners, expected_runners)

    def test_add_runners_when_race_contain_one_runner(self):
        # Setup
        id_fake = "R001"
        name_fake = "R001"
        runners_fake = build_runners(3)
        race = build_race(id=id_fake, name=name_fake,runners_fake=runners_fake)

        new_runners_fake = build_runners(3)
        race.add_runners(new_runners_fake)

        expected_runners = runners_fake + new_runners_fake

        # Assert
        self.assertEqual(race.is_sorted, False)

        self.assertEqual(len(race.runners), len(expected_runners))
        self.assertEqual(race.runners, expected_runners)

    def test_disqualified_runner(self):
        # Setup
        id_fake = "R001"
        name_fake = "R001"
        raw_ranking_fake = build_runners_race_ranking(3)
        runners_fake = build_runners(3)
        expected_raw_ranking_fake = copy.deepcopy(raw_ranking_fake)
        expected_raw_ranking_fake[0].is_disqualified = True

        race = build_race(id=id_fake, name=name_fake, runners_fake=runners_fake, raw_ranking_fake=raw_ranking_fake)

        # Act
        race.disqualified_runner(runners_fake[0])

        # Assert
        self.assertEqual(race.is_sorted, False)

        self.assertEqual(len(race.raw_ranking), len(expected_raw_ranking_fake))
        self.assertEqual(race.raw_ranking, expected_raw_ranking_fake)

    def test_ranking_return_all_runners_from_raw_ranking(self):
        # Setup
        id_fake = "R001"
        name_fake = "R001"
        raw_ranking_fake = build_runners_race_ranking(3)
        runners_fake = build_runners(3)
        race = build_race(id=id_fake, name=name_fake, runners_fake=runners_fake, raw_ranking_fake=raw_ranking_fake)

        expected_ranking = copy.deepcopy(raw_ranking_fake)

        # Act
        current_ranking = race.get_ranking()

        # Assert
        self.assertEqual(race.is_sorted, True)
        self.assertEqual(current_ranking, expected_ranking)

    def test_get_ranking_return_zero_runner_when_runners_is_zero(self):
        # Setup
        id_fake = "R001"
        name_fake = "R001"
        raw_ranking_fake = build_runners_race_ranking(3)
        race = build_race(id=id_fake, name=name_fake, raw_ranking_fake=raw_ranking_fake)

        # Act
        current_ranking = race.get_ranking()

        # Assert
        self.assertEqual(race.is_sorted, True)
        self.assertEqual(len(current_ranking), 0)

    def test_get_ranking_return_zero_runner_when_one_runner_not_finish_race(self):
        # Setup
        id_fake = "R001"
        name_fake = "R001"
        raw_ranking_fake = [build_runner_race_ranking(0, finished=False)]
        runners_fake = [build_runner(0)]
        race = build_race(id=id_fake, name=name_fake, raw_ranking_fake=raw_ranking_fake, runners_fake=runners_fake)

        # Act
        current_ranking = race.get_ranking()

        # Assert
        self.assertEqual(race.is_sorted, True)
        self.assertEqual(len(current_ranking), 0)

    def test_get_ranking_return_zero_runner_when_one_runner_is_finish_race(self):
        # Setup
        id_fake = "R001"
        name_fake = "R001"
        raw_ranking_fake = [build_runner_race_ranking(0, finished=False)]
        runners_fake = [build_runner(0)]
        race = build_race(id=id_fake, name=name_fake, raw_ranking_fake=raw_ranking_fake, runners_fake=runners_fake)

        # Act
        current_ranking = race.get_ranking()

        # Assert
        self.assertEqual(race.is_sorted, True)
        self.assertEqual(len(current_ranking), 0)

    def test_get_ranking_return_zero_runner_when_one_runner_is_disqualified(self):
        # Setup
        id_fake = "R001"
        name_fake = "R001"
        raw_ranking_fake = [build_runner_race_ranking(0, finished=False)]
        runners_fake = [build_runner(0)]

        expected_raw_ranking_fake = copy.deepcopy(raw_ranking_fake)
        expected_raw_ranking_fake[0].is_disqualified = True

        race = build_race(id=id_fake, name=name_fake, raw_ranking_fake=raw_ranking_fake, runners_fake=runners_fake)

        # Act
        race.disqualified_runner(runners_fake[0])
        current_ranking = race.get_ranking()

        # Assert
        self.assertEqual(race.is_sorted, True)
        self.assertEqual(len(current_ranking), 1)

    # Todo check set sorta and set point
