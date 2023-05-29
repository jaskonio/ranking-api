from app.model.RaceBaseModel import RaceBaseModel
from .MongoDBSession import get_database
from bson import ObjectId
from pymongo import collection

class RaceList:
    def __init__(self):
        collection_name = "RaceList"
        self.db = get_database()
        self.collection:collection.Collection = self.db[collection_name]

    def get_all(self):
        results = self.collection.find()
        
        leagues = []
        
        for result in results:
            leagues.append(RaceBaseModel.from_mongo(result))
        
        return leagues

    def add_race(self, race: RaceBaseModel):
        result = self.collection.insert_one(race.mongo())
        
        return result

    def get_by_id(self, str_id):
        race = self.collection.find_one({'_id': ObjectId(str_id)})

        return RaceBaseModel.from_mongo(race)

    def update_race(self, race_id, race:RaceBaseModel):
        race_dict = race.mongo()
        return self.collection.update_one({'_id': ObjectId(race_id)}, {'$set': race_dict})

    def delete_race(self, race_id):
        return self.collection.delete_one({"_id": ObjectId(race_id)})
