from typing import List
from app.domain.model.participant_league_model import ParticipantLeagueModel
from app.infrastructure.mongoDB.model.participant_league_entity import ParticipantLeagueEntity
from app.infrastructure.repository.repository_utils import load_repository_from_config


class ParticipantLeagueService():

    def __init__(self) -> None:
        db = load_repository_from_config()
        self.__person_repository = db.get_repository('participant_league', ParticipantLeagueEntity)

    def get_all(self) -> List[ParticipantLeagueModel]:
        participant_league_entity: List[ParticipantLeagueEntity] = self.__person_repository.get_all()
        return [participant_league_entity.to_domain_model(ParticipantLeagueModel) for participant_league_entity in participant_league_entity]

    def get_by_id(self, participant_id:str) -> ParticipantLeagueModel:
        participant_league_entity:ParticipantLeagueEntity = self.__person_repository.get_by_id(participant_id)

        if participant_league_entity is None:
            return None

        return participant_league_entity.to_domain_model(ParticipantLeagueModel)

    def add(self, new_person:ParticipantLeagueModel) -> ParticipantLeagueModel:
        participant_id = self.__person_repository.add(ParticipantLeagueEntity().create_by_domain_model(new_person))

        participant_league_entity:ParticipantLeagueEntity = self.__person_repository.get_by_id(participant_id)

        return participant_league_entity.to_domain_model(ParticipantLeagueModel)

    def update_by_id(self, participant_id:str, new_person:ParticipantLeagueModel):
        status = self.__person_repository.update_by_id(participant_id, ParticipantLeagueEntity().create_by_domain_model(new_person))

        if status:
            participant_league_entity:ParticipantLeagueEntity = self.__person_repository.get_by_id(participant_id)
            return participant_league_entity.to_domain_model(ParticipantLeagueModel)
        else:
            return None

    def delete_by_id(self, participant_id: str) -> bool:
        status = self.__person_repository.delete_by_id(participant_id)

        if status:
            return status

        return None
