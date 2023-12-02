class LeagueBuilder:
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