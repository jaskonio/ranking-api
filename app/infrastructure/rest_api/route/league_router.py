from typing import List
from fastapi import APIRouter
from app.aplication.league_service import LeagueService
from app.domain.model.league import League
from app.domain.model.person import Person
from app.domain.model.race import Race
from app.domain.model.runner_base import RunnerBase
from app.infrastructure.repository.repository_utils import load_repository_from_config
from app.infrastructure.rest_api.controller.league_controller import LeagueController
from app.infrastructure.rest_api.model.legaue_request import LeagueRequest
from app.infrastructure.rest_api.model.runner_request import RunnerRequest


league_router = APIRouter()

db = load_repository_from_config()
controller = LeagueController(LeagueService(db.get_repository('Leagues', League)
                                        , db.get_repository('Races', Race)
                                        , db.get_repository('Persons', Person)))

@league_router.get('/')
def get_all():
    return controller.get_all()

@league_router.get('/{league_id}')
def get_by_id(league_id:str):
    return controller.get_by_id(league_id)

@league_router.post('/')
def add(race: LeagueRequest):
    race_entity = race.to_entity(League)
    return controller.add(race_entity)

@league_router.post('/{league_id}/add_runners')
def add_runners(league_id:str, new_runners: List[RunnerRequest]):
    runners_entities = [runner.to_entity(RunnerBase) for runner in new_runners]
    return controller.add_runners(league_id, runners_entities)

@league_router.post('/{league_id}/add_runner')
def add_runner(league_id:str, new_runner: RunnerRequest):
    runner_entity = new_runner.to_entity(RunnerBase, 'person_id')
    return controller.add_runner(league_id, runner_entity)

@league_router.post('/{league_id}/delete_runners')
def delete_runners(league_id:str, runners: List[RunnerRequest]):
    return controller.delete_runners(league_id, runners)

@league_router.post('/{league_id}/delete_runner')
def delete_runner(league_id:str, new_runner: RunnerRequest):
    return controller.delete_runner(league_id, new_runner)

@league_router.get('/{league_id}/add_race/{race_id}/order/{order_race}')
def add_race(league_id:str, race_id: str, order_race:int):
    return controller.add_race(league_id, race_id, order_race)

@league_router.get('/{league_id}/disqualify_runner')
def disqualify_runner(league_id:str, race_name: str, bib_number:int):
    return controller.disqualify_runner(league_id, race_name, bib_number)

@league_router.put('/{league_id}')
def update_by_id(league_id: str, league: LeagueRequest):
    league_entity = league.to_entity(League)
    return controller.update_by_id(league_id, league_entity)

@league_router.delete('/{league_id}')
def delete_by_id(league_id:str):
    return controller.delete_by_id(league_id)
