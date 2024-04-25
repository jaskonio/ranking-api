from app.infrastructure.mongoDB.model.participant_league_entity import ParticipantLeagueModel


class ParticipantRaceEntityProperty(ParticipantLeagueModel):
    is_disqualified: bool = False
