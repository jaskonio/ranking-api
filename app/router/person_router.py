"""_summary_

Returns:
    _type_: _description_
"""
from app.controller.person_controller import PersonController
from app.infrastructure.mongoDB.person_list import PersonList
from app.model.person_model import PersonModel
from app.router.base_router import BaseRouter


class PersonRouter(BaseRouter):
    """_summary_

    Args:
        APIRouter (_type_): _description_
    """
    def __init__(self):
        super().__init__('person', PersonController(PersonList()), PersonModel)
