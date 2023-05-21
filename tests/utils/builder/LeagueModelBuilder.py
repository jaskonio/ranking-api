from app.model.LeagueModel import LeagueModel


class LeagueModelBuilder:
    def create_league_model_fake(self, races=[], runnerParticipants=[]):
        league_fake = {
            "name": "league_01",
            "races": races,
            "runnerParticipants": runnerParticipants
        }
        return LeagueModel(**dict(league_fake))
