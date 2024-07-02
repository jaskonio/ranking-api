import unittest
from unittest.mock import patch, MagicMock
from bson import ObjectId
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError
from app.domain.model.season_model import SeasonModel
from app.domain.model.league_model import LeagueModel
from app.infrastructure.exceptions import RepositoryConnectionError, RepositoryOperationError
from app.infrastructure.mongoDB.repository.seasson_repository import SeassonRepository
from app.infrastructure.mongoDB.repository.league_repository import LeagueRepository

class TestSeassonRepository(unittest.TestCase):
    @patch('app.infrastructure.mongoDB.repository.mongo_db_repository.MongoDBSession.get_collection')
    def setUp(self, mock_get_collection):
        self.mock_collection = MagicMock()
        mock_get_collection.return_value = self.mock_collection

        self.mock_league_repository = MagicMock(spec=LeagueRepository)

        self.season_repository = SeassonRepository(
            league_repository=self.mock_league_repository
        )

    def test_get_all_empty(self):
        self.mock_collection.find.return_value = []
        self.mock_league_repository.get_all.return_value = []

        result = self.season_repository.get_all()
        self.assertEqual(result, [])

    def test_get_all(self):
        season_data = {"_id": ObjectId(), "name": "Test Season", "order": 1, "league_ids": [str(ObjectId())]}
        league_data = LeagueModel(id=str(ObjectId()), name="Test League", order=1)
        
        self.mock_collection.find.return_value = [season_data]
        self.mock_league_repository.get_all.return_value = [league_data]

        result = self.season_repository.get_all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Test Season")

    def test_get_by_id_not_found(self):
        self.mock_collection.find_one.return_value = None

        result = self.season_repository.get_by_id(str(ObjectId()))
        self.assertIsNone(result)

    def test_get_by_id(self):
        season_data = {"_id": ObjectId(), "name": "Test Season", "order": 1, "league_ids": [str(ObjectId())]}
        league_data = LeagueModel(id=str(ObjectId()), name="Test League", order=1)
        
        self.mock_collection.find_one.return_value = season_data
        self.mock_league_repository.get_all.return_value = [league_data]

        result = self.season_repository.get_by_id(str(ObjectId()))
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Test Season")

    def test_update_by_id_success(self):
        season_model = SeasonModel(id=str(ObjectId()), name="Updated Season", order=2)
        league_model = LeagueModel(id=str(ObjectId()), name="Updated League", order=1)
        season_model.leagues = [league_model]

        self.mock_collection.update_one.return_value = MagicMock(matched_count=1)
        self.mock_collection.find_one.return_value = {
            "_id": ObjectId(season_model.id),
            "name": season_model.name,
            "order": season_model.order,
            "league_ids": [league_model.id]
        }

        result = self.season_repository.update_by_id(str(ObjectId()), season_model)
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Updated Season")

    # Exceptions

    def test_get_all_connection_error(self):
        self.mock_collection.find.side_effect = ServerSelectionTimeoutError("Timeout error")
        
        with self.assertRaises(RepositoryConnectionError):
            self.season_repository.get_all()

    def test_get_all_operation_error(self):
        self.mock_collection.find.side_effect = PyMongoError("General error")
        
        with self.assertRaises(RepositoryOperationError):
            self.season_repository.get_all()

    def test_get_by_id_connection_error(self):
        self.mock_collection.find_one.side_effect = ServerSelectionTimeoutError("Timeout error")
        
        with self.assertRaises(RepositoryConnectionError):
            self.season_repository.get_by_id(str(ObjectId()))

    def test_get_by_id_operation_error(self):
        self.mock_collection.find_one.side_effect = PyMongoError("General error")
        
        with self.assertRaises(RepositoryOperationError):
            self.season_repository.get_by_id(str(ObjectId()))

    def test_update_by_id_connection_error(self):
        season_model = SeasonModel(id=str(ObjectId()), name="Updated Season", order=2)
        league_model = LeagueModel(id=str(ObjectId()), name="Updated League", order=1)
        season_model.leagues = [league_model]

        self.mock_collection.update_one.side_effect = ServerSelectionTimeoutError("Timeout error")
        
        with self.assertRaises(RepositoryConnectionError):
            self.season_repository.update_by_id(str(ObjectId()), season_model)

    def test_update_by_id_operation_error(self):
        season_model = SeasonModel(id=str(ObjectId()), name="Updated Season", order=2)
        league_model = LeagueModel(id=str(ObjectId()), name="Updated League", order=1)
        season_model.leagues = [league_model]

        self.mock_collection.update_one.side_effect = PyMongoError("General error")
        
        with self.assertRaises(RepositoryOperationError):
            self.season_repository.update_by_id(str(ObjectId()), season_model)

if __name__ == '__main__':
    unittest.main()
