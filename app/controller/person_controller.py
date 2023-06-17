"""
    TODO
"""
from app.controller.base_controller import BaseController
from app.infrastructure.mongoDB.person_list import PersonList


class PersonController(BaseController):
    """_summary_
    """
    def __init__(self, runner_repository:PersonList):
        super().__init__(runner_repository)
