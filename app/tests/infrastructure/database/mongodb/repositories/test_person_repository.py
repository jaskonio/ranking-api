import unittest
from unittest.mock import patch, MagicMock
from bson import ObjectId
import mongomock
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError
from app.domain.model.person_model import PersonModel
from app.infrastructure.mongoDB.model.person_entity import PersonEntity
from app.infrastructure.mongoDB.repository.person_repository import PersonRepository
from app.infrastructure.exceptions import RepositoryConnectionError, RepositoryOperationError, RepositoryNotFoundError

# Mocks para el modelo de dominio y la entidad
class MockModel(PersonModel):
    id: str = ''
    first_name: str = 'John'
    last_name: str = 'Doe'
    full_name: str = ''

    def set_full_name(self):
        self.full_name = f"{self.first_name} {self.last_name}"

class MockEntity(PersonEntity):
    id: str = ''
    first_name: str = 'John'
    last_name: str = 'Doe'

    @staticmethod
    def create_by_domain_model(domain_model: PersonModel):
        return MockEntity(id=domain_model.id, first_name=domain_model.first_name, last_name=domain_model.last_name)

    def to_domain_model(self, model_type: PersonModel):
        model:PersonModel = model_type(id=self.id, first_name=self.first_name, last_name=self.last_name)
        model.set_full_name()
        return model

class TestPersonRepository(unittest.TestCase):

    @patch('app.infrastructure.mongoDB.repository.mongo_db_session.MongoDBSession.get_collection')
    def setUp(self, mock_get_collection):
        # Mock de la colección MongoDB
        self.mock_collection = mongomock.MongoClient().db.person
        mock_get_collection.return_value = self.mock_collection

        # Inicializar el repositorio
        self.repository = PersonRepository()

    def test_get_all(self):
        # Insertar datos simulados
        self.mock_collection.insert_one({'_id': ObjectId(), 'first_name': 'John', 'last_name': 'Doe'})

        # Llamar al método
        result = self.repository.get_all()

        # Verificar las aserciones
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].first_name, 'John')
        self.assertEqual(result[0].last_name, 'Doe')
        self.assertEqual(result[0].full_name, 'John Doe')

    def test_get_by_id(self):
        # Insertar datos simulados
        mock_id = ObjectId()
        self.mock_collection.insert_one({'_id': mock_id, 'first_name': 'John', 'last_name': 'Doe'})

        # Llamar al método
        result = self.repository.get_by_id(str(mock_id))

        # Verificar las aserciones
        self.assertIsNotNone(result)
        self.assertEqual(result.first_name, 'John')
        self.assertEqual(result.last_name, 'Doe')
        self.assertEqual(result.full_name, 'John Doe')

    def test_get_by_id_not_found(self):
        # Call the method with a non-existing ID
        result = self.repository.delete_by_id(str(ObjectId()))

        # Check assertions
        self.assertFalse(result)

    # Exceptions
    def test_get_all_connection_error(self):
        with patch.object(self.mock_collection, 'find', side_effect=ServerSelectionTimeoutError):
            with self.assertRaises(RepositoryConnectionError):
                self.repository.get_all()

    def test_get_all_operation_error(self):
        with patch.object(self.mock_collection, 'find', side_effect=PyMongoError):
            with self.assertRaises(RepositoryOperationError):
                self.repository.get_all()

    def test_get_by_id_connection_error(self):
        with patch.object(self.mock_collection, 'find_one', side_effect=ServerSelectionTimeoutError):
            with self.assertRaises(RepositoryConnectionError):
                self.repository.get_by_id(str(ObjectId()))

    def test_get_by_id_operation_error(self):
        with patch.object(self.mock_collection, 'find_one', side_effect=PyMongoError):
            with self.assertRaises(RepositoryOperationError):
                self.repository.get_by_id(str(ObjectId()))

if __name__ == '__main__':
    unittest.main()
