import logging
from typing import List
from app.aplication.iservice import IGenericService
from app.aplication.league_service import LeagueService
from app.domain.model.league_model import LeagueRAWModel
from app.domain.model.person_model import PersonModel
from app.domain.repository.igeneric_repository import IGenericRepository
from app.infrastructure.rest_api.controller.base_controller import BaseController
from app.infrastructure.rest_api.model.custom_responses import CustomStaticJSONResponse
from app.infrastructure.rest_api.model.league_model import LeagueRawResponse, LeagueRequest, LeagueResponse, RunnerParticipantLeague


class LeagueController(BaseController):
    def __init__(self, league_service:LeagueService, api_model, domain_model, person_service:IGenericService):
        super().__init__(league_service, api_model, domain_model)
        self.logger = logging.getLogger(__name__)
        self.__league_service = league_service
        self.__person_service = person_service

    def get_all(self):
        try:
            league_models = self.base_service.get_all()
            all_persons:List[PersonModel] = self.__person_service.get_all()

            leagues_response = []
            for league_model in league_models:
                league_response = LeagueResponse().create_by_domain_model(league_model)
                
                runner_participant_merged = []
                participant_ids = [p.person_id for p in league_response.runner_participants]
                persons_in_league = list(filter(lambda p: p.id in participant_ids, all_persons))
                for runner_participant in league_response.runner_participants:
                    for person_in_league in persons_in_league:
                        if runner_participant.person_id == person_in_league.id:
                            runner_participant_dict = runner_participant.dict()
                            person_in_league_dict = person_in_league.dict()
                            runner_participant_dict.update(person_in_league_dict)
                            runner_participant = RunnerParticipantLeague(**runner_participant_dict)
                            runner_participant_merged.append(runner_participant)
                league_response.runner_participants = runner_participant_merged

                leagues_response.append(league_response)

            return CustomStaticJSONResponse.success(data=leagues_response)
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")

    def get_by_id(self, model_id):
        try:
            league_model = self.base_service.get_by_id(model_id)
            all_persons:List[PersonModel] = self.__person_service.get_all()
            
            league_response = LeagueResponse().create_by_domain_model(league_model)
                
            runner_participant_merged = []
            participant_ids = [p.person_id for p in league_response.runner_participants]
            persons_in_league = list(filter(lambda p: p.id in participant_ids, all_persons))
            for runner_participant in league_response.runner_participants:
                for person_in_league in persons_in_league:
                    if runner_participant.person_id == person_in_league.id:
                        runner_participant_dict = runner_participant.dict()
                        person_in_league_dict = person_in_league.dict()
                        runner_participant_dict.update(person_in_league_dict)
                        runner_participant = RunnerParticipantLeague(**runner_participant_dict)
                        runner_participant_merged.append(runner_participant)
            league_response.runner_participants = runner_participant_merged

            return CustomStaticJSONResponse.success(data=league_response)
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")

    def get_all_raw(self):
        try:
            models: List[LeagueRAWModel] = self.__league_service.get_all_raw()
            results = [LeagueRawResponse().create_by_domain_model(model) for model in models]
            return CustomStaticJSONResponse.success(data=results)
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")

    def get_raw_by_id(self, league_id:str):
        try:
            league_model = self.__league_service.get_raw_by_id(league_id)

            if league_model is None:
                return CustomStaticJSONResponse.error(status_code=404, message=f"El ID {league_id} no se ha encontrado")

            results = LeagueRawResponse().create_by_domain_model(league_model)

            return CustomStaticJSONResponse.success(data=results)
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")

    def run_process_by_id(self, league_id:str) -> LeagueRawResponse:
        try:
            league_model = self.__league_service.run_process(league_id)

            if league_model:
                return CustomStaticJSONResponse.error(status_code=404, message=f"El ID {league_id} no se ha encontrado")

            result = LeagueRawResponse().create_by_domain_model(league_model)

            return CustomStaticJSONResponse.success(data=result)
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")
