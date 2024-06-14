import logging
from typing import List
from app.aplication.league_service import LeagueService
from app.domain.model.league_model import LeagueRace, LeagueModel, ParticipantLeagueModel
from app.domain.model.person_model import PersonModel
from app.domain.model.race_info_model import RaceModel
from app.domain.repository.igeneric_repository import IGenericRepository
from app.infrastructure.mongoDB.repository.race_info_repository import RaceInfoRepository
from app.infrastructure.rest_api.controller.base_controller import BaseController
from app.infrastructure.rest_api.model.custom_responses import CustomStaticJSONResponse
from app.infrastructure.rest_api.model.league_model import LeagueResponse, LeagueRequest 


class LeagueController(BaseController):
    def __init__(self, league_service:LeagueService, api_model, domain_model, race_services_repository:RaceInfoRepository, person_repository:IGenericRepository):
        super().__init__(league_service, api_model, domain_model)
        self.logger = logging.getLogger(__name__)
        self.__league_service = league_service
        self.__race_info_repository = race_services_repository
        self.__person_repository = person_repository

    def update_by_id(self, model_id:str, new_model: LeagueRequest):
        try:
            all_race_info:List[RaceModel] = self.__race_info_repository.get_all()
            races:List[LeagueRace] = []

            for race_info in all_race_info:
                if new_model.races is not None:
                    for race in new_model.races:
                        if race_info.id == race.race_info_id:
                            new_races = LeagueRace(**race_info.dict())
                            new_races.order = race.order
                            races.append(new_races)

            all_persons:List[PersonModel] = self.__person_repository.get_all()
            runner_participants:List[ParticipantLeagueModel] = []

            for person in all_persons:
                if new_model.runner_participants is not None:
                    for league_runner_participant in new_model.runner_participants:
                        if person.id == league_runner_participant.person_id:
                            new_runner_participant = ParticipantLeagueModel(**person.dict())
                            new_runner_participant.person_id = league_runner_participant.person_id
                            new_runner_participant.dorsal = league_runner_participant.dorsal
                            new_runner_participant.category= league_runner_participant.category
                            new_runner_participant.disqualified_order_race= league_runner_participant.disqualified_order_race
                            new_runner_participant.unique_dorsal = league_runner_participant.unique_dorsal
                            runner_participants.append(new_runner_participant)

            domain_model = LeagueModel(name=new_model.name,
                                       order=new_model.order,
                                       races=races,
                                       runner_participants=runner_participants)

            result_model_domain = self.__league_service.update_by_id(model_id, domain_model)

            if result_model_domain is None:
                return CustomStaticJSONResponse.error(status_code=404, message=f"El ID {model_id} no se ha encontrado")

            return CustomStaticJSONResponse.success(data=self.api_response_model().create_by_domain_model(result_model_domain))
        except Exception as exception_error:
            self.logger.error("Error updating: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")

    def run_process_by_id(self, league_id:str) -> LeagueResponse:
        try:
            league_model = self.__league_service.run_process(league_id)

            if league_model is None:
                return CustomStaticJSONResponse.error(status_code=404, message=f"El ID {league_id} no se ha encontrado")

            result = LeagueResponse().create_by_domain_model(league_model)

            return CustomStaticJSONResponse.success(data=result)
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")
