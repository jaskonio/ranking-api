from .MongoDBSession import get_database
from bson import ObjectId
from pymongo import collection, database
from app.model.LeagueModel import LeagueModel


class LeagueList:
    def __init__(self):
        collection_name = "LeagueList"
        self.database:database.Database = get_database()
        self.collection:collection.Collection = self.database.get_collection(collection_name)

    def get_all(self):
        results = self.collection.find()

        leagues = []

        for result in results:
            leagues.append(LeagueModel.from_mongo(result))

        return leagues

    def add_legue(self, league: LeagueModel):
        result = self.collection.insert_one(league.mongo())

        return result

    def get_by_id(self, str_id):
        league = self.collection.find_one({'_id': ObjectId(str_id)})

        return LeagueModel.from_mongo(league)

    def update_league(self, league_id, league:LeagueModel):
        league_dict = league.mongo()
        return self.collection.update_one({'_id': ObjectId(league_id)}, {'$set': league_dict})

    def delete_league(self, league_id):
        return self.collection.delete_one({"_id": ObjectId(league_id)})
