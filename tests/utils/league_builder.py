from typing import List
from app.domain.model.league import League
from app.domain.model.race import Race
from app.domain.model.runner_base import RunnerBase
from app.domain.model.runner_league_ranking import RunnerLeagueRanking


class LeagueBuilder:
    def __init__(self, id:str='0', name:str='league_01', races: List[Race] = None, ranking:List[RunnerLeagueRanking] = None
                 , participants: List[RunnerBase] = None ):
        self.id = str(id)
        self.name = name
        self.races:List[Race] = races
        self.ranking:List[RunnerLeagueRanking] = ranking
        self.participants:List[RunnerBase] = participants

    def with_id(self, id):
        self.id = str(id)
        return self

    def with_name(self, name):
        self.name = name
        return self

    def with_races(self, races):
        self.races = races
        return self

    def with_ranking(self, ranking):
        self.ranking = ranking
        return self

    def with_participants(self, participants):
        self.participants = participants
        return self

    def build(self):
        return League(
            id=self.id,
            name=self.name,
            races=self.races,
            ranking=self.ranking,
            participants=self.participants
        )
