from app.domain.model.race import Race

class RaceBuilder:
    def __init__(self, id=1, name='Test Race', url='test_url', raw_ranking=None, platform_inscriptions=None,
                 order=0, is_sorted=False, ranking=None, participants=None):
        self.id = id
        self.name = name
        self.url = url
        self.raw_ranking = raw_ranking if raw_ranking is not None else []
        self.platform_inscriptions = platform_inscriptions
        self.order = order
        self.is_sorted = is_sorted
        self.ranking = ranking if ranking is not None else []
        self.participants = participants if participants is not None else []

    def with_raw_ranking(self, runner):
        self.raw_ranking = runner
        return self

    def with_platform_inscriptions(self, platform_inscriptions):
        self.platform_inscriptions = platform_inscriptions
        return self

    def with_order(self, runner):
        self.order = runner
        return self

    def with_is_sorted(self, runner):
        self.is_sorted = runner
        return self

    def with_ranking(self, ranking):
        self.ranking = ranking
        return self

    def with_participant(self, runner):
        self.participants = runner
        return self

    def build(self):
        return Race(
            id=self.id,
            name=self.name,
            url=self.url,
            raw_ranking=self.raw_ranking,
            platform_inscriptions=self.platform_inscriptions,
            order=self.order,
            is_sorted=self.is_sorted,
            ranking=self.ranking,
            participants=self.participants
        )
