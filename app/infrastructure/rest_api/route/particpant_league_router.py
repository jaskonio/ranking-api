from typing import List
from fastapi import APIRouter
from app.domain.model.participant_league_model import ParticipantLeagueModel
from app.infrastructure.mongoDB.model.participant_league_entity import ParticipantLeagueEntity
from app.infrastructure.rest_api.controller.base_controller import BaseController
from app.infrastructure.rest_api.model.participant_league_model import ParticipantLeagueRequest, ParticipantLeagueResponse
from app.core.services import participant_league_service

participant_league_router = APIRouter()

controller = BaseController(participant_league_service, ParticipantLeagueModel, ParticipantLeagueEntity)

@participant_league_router.get('/')
def get_all() -> List[ParticipantLeagueResponse]:
    return controller.get_all()

@participant_league_router.get('/{person_id}')
def get_by_id(person_id:str) -> ParticipantLeagueResponse:
    return controller.get_by_id(person_id)

@participant_league_router.post('/')
def add(new_person: ParticipantLeagueRequest) -> ParticipantLeagueResponse:
    return controller.add(new_person)

@participant_league_router.put('/{person_id}')
def update_by_id(person_id: str, person: ParticipantLeagueRequest) -> ParticipantLeagueResponse:
    return controller.update_by_id(person_id, person)

@participant_league_router.delete('/{person_id}')
def delete_by_id(person_id:str) -> bool:
    return controller.delete_by_id(person_id)
