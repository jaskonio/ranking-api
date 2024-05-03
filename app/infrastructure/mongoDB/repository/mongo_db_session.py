from pymongo import MongoClient
from app.core.config import Settings
from app.domain.repository.igeneric_repository import IGenericRepository
from app.infrastructure.mongoDB.model.club_info_entity import ClubInfoEntity
from app.infrastructure.mongoDB.model.league_entity import LeagueEntity
from app.infrastructure.mongoDB.model.participant_league_entity import ParticipantLeagueEntity
from app.infrastructure.mongoDB.model.person_entity import PersonEntity
from app.infrastructure.mongoDB.model.race_data_entity import RaceDataEntity
from app.infrastructure.mongoDB.model.race_info_entity import RaceInfoEntity
from app.infrastructure.mongoDB.model.race_league_entity import RaceLeagueEntity
from app.infrastructure.mongoDB.model.ranking_league_entity import RankingLeagueEntity
from app.infrastructure.mongoDB.model.runner_race_data_entity import RunnerRaceDataEntity
from app.infrastructure.mongoDB.model.season_entity import SeasonEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository

class MongoDBSession:
    def __init__(self):
        db_name = Settings.DATABASE_NAME
        connection_string = Settings.CONNECTION_STRING + db_name

        self.client = MongoClient(connection_string)
        self.database = self.client.get_database()

db = MongoDBSession()
