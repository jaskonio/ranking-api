from typing import List
from app.domain.model.race import Race
from tests.utils.runner_race_ranking_utils import build_runners_race_ranking
from tests.utils.runner_utils import build_runners



def build_races(limit_races, limit_raw_runners=5, limit_runners=3):
    races:List[Race] = []

    for num in range(0,limit_races):
        raw_ranking_fake = build_runners_race_ranking(limit_raw_runners)
        runners_fake = build_runners(limit_runners)
        id = "id_00" + str(num)
        name = "name_00" + str(num)
        url = "url_00" + str(num)
        order = num
        race = build_race(id, name, url, raw_ranking_fake=raw_ranking_fake, runners_fake=runners_fake, order=order)
        races.append(race)

    return races

def build_race(id="R001", name="RName001", url="R_url_001", runners_fake=[], raw_ranking_fake=[], ranking_fake=[], order=0, is_sorted=False):
    return Race(
        id=id,
        name=name,
        url=url,
        is_sorted=is_sorted,
        order=order,
        raw_ranking=raw_ranking_fake,
        runners=runners_fake,
        ranking=ranking_fake
        )
