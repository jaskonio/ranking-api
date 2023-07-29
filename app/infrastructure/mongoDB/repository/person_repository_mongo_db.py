from ast import List
from pymongo import collection
from app.domain.model.person import Person
from app.domain.repository.person_repository import PersonRepository
from app.infrastructure.mongoDB.MongoDBSession import get_database
from app.infrastructure.mongoDB.model.person_model import PersonModel


class PersonRepositoryMongoDB(PersonRepository):
    def __init__(self, collection_name):
        name = collection_name
        self.database = get_database()
        self.collection:collection.Collection = self.database.get_collection(name)

    def get_all(self):
        persons_model = self.collection.find()

        persons = []

        for result in persons_model:
            person_model = PersonModel.from_mongo(result)
            persons.append(dict(person_model))

        return persons
