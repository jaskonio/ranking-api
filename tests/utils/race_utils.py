from typing import List
from app.domain.model.race import Race
from tests.utils.race_builder import RaceBuilder
from tests.utils.runner_race_ranking_utils import build_runners_race_ranking

def build_races(limit_races, limit_raw_runners=5, limit_runners=3):
    races:List[Race] = []

    for num in range(0,limit_races):

        id = "id_00" + str(num)
        name = "name_00" + str(num)
        url = "url_00" + str(num)
        raw_ranking_fake = build_runners_race_ranking(limit_raw_runners)
        order = num
        is_sorted = False
        ranking = []
        participants = []

        race = RaceBuilder(id, name, url).with_raw_ranking(raw_ranking_fake).with_order(order).with_is_sorted(is_sorted).with_ranking(ranking).with_participant(participants).build()

        races.append(race)

    return races
