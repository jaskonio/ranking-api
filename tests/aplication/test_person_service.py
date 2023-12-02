import unittest
from unittest.mock import MagicMock
from app.aplication.person_service import PersonService
from app.domain.repository.igeneric_repository import IGenericRepository
from tests.utils.person_builder import PersonBuilder


class TestPersonService(unittest.TestCase):
    def setUp(self):
        self.person_repository_mock = MagicMock(spec=IGenericRepository)
        self.person_service = PersonService(person_repository=self.person_repository_mock)

    def test_get_all(self):
        # Mocking the person_repository.get_all method
        fake_person = PersonBuilder().build()
        self.person_repository_mock.get_all.return_value = [fake_person]

        # Testing the get_all method
        result = self.person_service.get_all()

        # Assertions
        self.assertEqual(result, [fake_person])
        self.person_repository_mock.get_all.assert_called_once()

    def test_get_by_id(self):
        # Mocking the person_repository.get_by_id method
        fake_person = PersonBuilder().with_id(1).build()
        self.person_repository_mock.get_by_id.return_value = fake_person

        # Testing the get_by_id method
        result = self.person_service.get_by_id(1)

        # Assertions
        self.assertEqual(result, fake_person)
        self.person_repository_mock.get_by_id.assert_called_once_with(1)

    def test_add(self):
        # Mocking the person_repository.add and person_repository.get_by_id methods
        fake_person_id = 1
        fake_person = PersonBuilder().with_id(fake_person_id).build()

        self.person_repository_mock.add.return_value = fake_person_id
        self.person_repository_mock.get_by_id.return_value = fake_person

        # Testing the add method
        result = self.person_service.add(fake_person)

        # Assertions
        self.assertEqual(result, fake_person)
        self.person_repository_mock.add.assert_called_once_with(fake_person)
        self.person_repository_mock.get_by_id.assert_called_once_with(fake_person_id)

    def test_update_by_id(self):
        # Mocking the person_repository.update_by_id and person_repository.get_by_id methods
        fake_person_id = 1
        fake_person = PersonBuilder().with_id(fake_person_id).build()

        self.person_repository_mock.update_by_id.return_value = True
        self.person_repository_mock.get_by_id.return_value = fake_person

        # Testing the update_by_id method
        result = self.person_service.update_by_id(1, fake_person)

        # Assertions
        self.assertEqual(result, fake_person)
        self.person_repository_mock.update_by_id.assert_called_once_with(1, fake_person)
        self.person_repository_mock.get_by_id.assert_called_once_with(1)

    def test_update_by_id_failure(self):
        # Mocking the person_repository.update_by_id method that returns False
        fake_person_id = 1
        fake_person = PersonBuilder().with_id(fake_person_id).build()

        self.person_repository_mock.update_by_id.return_value = False

        # Testing the update_by_id method when update fails
        result = self.person_service.update_by_id(1, fake_person)

        # Assertions
        self.assertIsNone(result)
        self.person_repository_mock.update_by_id.assert_called_once_with(1, fake_person)
        self.person_repository_mock.get_by_id.assert_not_called()

    def test_delete_by_id(self):
        # Mocking the person_repository.delete_by_id method
        self.person_repository_mock.delete_by_id.return_value = True

        # Testing the delete_by_id method
        result = self.person_service.delete_by_id(1)

        # Assertions
        self.assertTrue(result)
        self.person_repository_mock.delete_by_id.assert_called_once_with(1)

    def test_delete_by_id_failure(self):
        # Mocking the person_repository.delete_by_id method that returns False
        self.person_repository_mock.delete_by_id.return_value = False

        # Testing the delete_by_id method when delete fails
        result = self.person_service.delete_by_id(1)

        # Assertions
        self.assertFalse(result)
        self.person_repository_mock.delete_by_id.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
