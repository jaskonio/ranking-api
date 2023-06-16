"""_summary_

Returns:
    _type_: _description_
"""
from fastapi import APIRouter, Depends
from app.auth.auth_bearer import JWTBearer
from app.controller.person_controller import PersonController
from app.core.cache import local_cache
from app.infrastructure.mongoDB.person_list import PersonList
from app.model.person_model import PersonModel

person_router = APIRouter()

controller = PersonController(PersonList())

# Rutas de la API
@person_router.get('/')
def get_all():
    """_summary_

    Returns:
        _type_: _description_
    """
    key = "runners/"
    data = local_cache.get(key)

    if not data:
        data = controller.get_all()
        local_cache.add(key, data)

    return data

@person_router.post('/', dependencies=[Depends(JWTBearer())])
def add(runner: PersonModel):
    """_summary_

    Args:
        runners (LeagueModel): _description_

    Returns:
        _type_: _description_
    """
    new_runners = controller.add(runner)
    key = "runners/"
    local_cache.delete(key)

    return new_runners

@person_router.get('/{runner_id}')
def get_by_id(runner_id: str):
    """_summary_

    Args:
        runners_id (str): _description_

    Returns:
        _type_: _description_
    """
    key = "runners/%s",str(runner_id)
    data = local_cache.get(key)

    if not data:
        data = controller.get_by_id(runner_id)
        local_cache.add(key, data)

    return data

@person_router.put('/', dependencies=[Depends(JWTBearer())])
def update_runner(runner_id: str, new_runner: PersonModel):
    """_summary_

    Args:
        runners_id (str): _description_
        runners (LeagueModel): _description_

    Returns:
        _type_: _description_
    """
    return controller.update_runner(runner_id, new_runner)

@person_router.delete('/{runner_id}', dependencies=[Depends(JWTBearer())])
def delete_runner(runner_id: str):
    """_summary_

    Args:
        runners_id (str): _description_

    Returns:
        _type_: _description_
    """
    result = controller.delete_runner(runner_id)

    key = "runners/"
    local_cache.delete(key)

    return result
