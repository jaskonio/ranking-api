from app.model.LeagueModel import LeagueModel


class LeagueModelBuilder:
    def create_league_model_fake(self, name="123", races=[], runnerParticipants=[]):
        league_fake = {
            "name": name,
            "races": races,
            "runnerParticipants": runnerParticipants
        }
        return LeagueModel(**dict(league_fake))
