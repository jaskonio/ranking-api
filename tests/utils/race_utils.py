from app.domain.model.race import Race


def build_race(id, name="", url="", runners_fake=[], raw_ranking_fake=[], ranking_fake=[]):
    return Race(
        id=id,
        name=name,
        url=url,
        is_sorted=False,
        order=0,
        raw_ranking=raw_ranking_fake,
        runners=runners_fake,
        ranking=ranking_fake
        )
