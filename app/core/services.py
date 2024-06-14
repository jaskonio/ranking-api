from app.aplication.base_service import BaseService
from app.aplication.league_service import LeagueService
from app.aplication.race_info_service import RaceInfoService
from app.domain.model.club_info_model import ClubInfoModel
from app.domain.model.league_model import ParticipantLeagueModel
from app.domain.model.person_model import PersonModel
from app.domain.services.downloader_runners_service import DownloaderRunnersService
from app.infrastructure.cloud.aws_repository import AWS_Repository
from app.infrastructure.mongoDB.model.club_info_entity import ClubInfoEntity
from app.infrastructure.mongoDB.model.participant_league_entity import ParticipantLeagueEntity
from app.infrastructure.mongoDB.model.person_entity import PersonEntity
from app.infrastructure.mongoDB.repository.league_repository import LeagueRepository
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository
from app.infrastructure.mongoDB.repository.race_data_repository import RaceDataRepository
from app.infrastructure.mongoDB.repository.race_info_repository import RaceInfoRepository
from app.infrastructure.mongoDB.repository.ranking_league_repository import RankingLeagueRepository
from app.infrastructure.mongoDB.repository.seasson_repository import SeassonRepository


club_info_repository = MongoDBRepository('club_info', ClubInfoEntity, ClubInfoModel)
person_repository = MongoDBRepository('person', PersonEntity, PersonModel)
aws_repository = AWS_Repository()

race_data_repository = RaceDataRepository()
race_info_repository = RaceInfoRepository(race_data_repository)

participant_league_repository = MongoDBRepository('participant_league', ParticipantLeagueEntity, ParticipantLeagueModel)
 
ranking_league_repository = RankingLeagueRepository()
league_repository = LeagueRepository(race_info_repository, person_repository, ranking_league_repository)
season_repository = SeassonRepository(league_repository)

# club_service = BaseService(club_info_repository, PersonModel, ClubInfoEntity)
person_service = BaseService(person_repository)
participant_league_service = BaseService(participant_league_repository)
ranking_league_service = BaseService(ranking_league_repository)
seasson_service = BaseService(season_repository)

downloader_runners_service = DownloaderRunnersService(club_info_repository)
race_info_service = RaceInfoService(race_info_repository, downloader_runners_service, race_data_repository)
league_service = LeagueService(league_repository, ranking_league_repository, race_data_repository)
