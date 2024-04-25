from typing import List
from fastapi import APIRouter
from app.aplication.league_service import LeagueService
from app.infrastructure.rest_api.controller.league_controller import LeagueController
from app.infrastructure.rest_api.model.league_model import LeagueRequest, LeagueResponse


league_router = APIRouter()

controller = LeagueController(LeagueService())

@league_router.get('/')
def get_all() -> List[LeagueResponse]:
    return controller.get_all()

@league_router.post('/')
def add(new_league: LeagueRequest) -> LeagueResponse:
    return controller.add(new_league)

@league_router.get('/{league_id}')
def get_by_id(league_id:str) -> LeagueResponse:
    return controller.get_by_id(league_id)

@league_router.put('/{league_id}')
def update_by_id(league_id: str, league: LeagueRequest):
    return controller.update_by_id(league_id, league)

@league_router.delete('/{league_id}')
def delete_by_id(league_id:str):
    return controller.delete_by_id(league_id)

# @league_router.post('/{league_id}/add_runners')
# def add_runners(league_id:str, new_runners: List[RunnerBaseRequest]):
#     runners_entities = [runner.to_entity(RunnerBase) for runner in new_runners]
#     return controller.add_runners(league_id, runners_entities)

# @league_router.post('/{league_id}/add_runner')
# def add_runner(league_id:str, new_runner: RunnerBaseRequest):
#     runner_entity = new_runner.to_entity(RunnerBase, 'person_id')
#     return controller.add_runner(league_id, runner_entity)

# @league_router.post('/{league_id}/delete_runners')
# def delete_runners(league_id:str, runners: List[RunnerBaseRequest]):
#     return controller.delete_runners(league_id, runners)

# @league_router.post('/{league_id}/delete_runner')
# def delete_runner(league_id:str, new_runner: RunnerBaseRequest):
#     return controller.delete_runner(league_id, new_runner)

# @league_router.get('/{league_id}/add_race/{race_id}/order/{order_race}')
# def add_race(league_id:str, race_id: str, order_race:int):
#     return controller.add_race(league_id, race_id, order_race)

# @league_router.get('/{league_id}/disqualify_runner')
# def disqualify_runner(league_id:str, race_name: str, bib_number:int):
#     return controller.disqualify_runner(league_id, race_name, bib_number)
