from app.aplication.base_service import BaseService
from app.domain.model.person_model import PersonModel
from app.domain.model.race_info_model import RaceInfoModel
from app.domain.model.season_model import SeasonModel
from app.infrastructure.cloud.aws_repository import AWS_Repository
from app.infrastructure.mongoDB.model.club_info_entity import ClubInfoEntity
from app.infrastructure.mongoDB.model.person_entity import PersonEntity
from app.infrastructure.mongoDB.model.race_info_entity import RaceInfoEntity
from app.infrastructure.mongoDB.model.season_entity import SeasonEntity
from app.infrastructure.mongoDB.mongo_db_session import get_repository


club_info_repository = get_repository('club_info')
race_info_repository = get_repository('race_info')
person_repository = get_repository('person')
season_repository = get_repository('season')
race_league_repository = get_repository('race_league')
race_data_repository = get_repository('race_data')
runner_race_data_repository = get_repository('runner_race_data')
league_repository = get_repository('league')
ranking_league_repository = get_repository('ranking_league')
participant_league_repository = get_repository('participant_league')
aws_repository = AWS_Repository()

# club_service = BaseService(club_info_repository, PersonModel, ClubInfoEntity)
# race_info_service = BaseService(race_info_repository, RaceInfoModel, RaceInfoEntity)
person_service = BaseService(person_repository, PersonModel, PersonEntity)
seasson_service = BaseService(season_repository, SeasonModel, SeasonEntity)
