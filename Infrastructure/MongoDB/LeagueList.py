from Infrastructure.MongoDB.MongoDBSession import get_database
from Model.LeagueModel import LeagueModel
from bson import ObjectId
from pymongo import collection

class LeagueList:
    def __init__(self):
        collection_name = "LeagueList"
        self.db = get_database()
        self.collection:collection.Collection = self.db[collection_name]  # Obtener la colección

    def get_all(self):
        results = self.collection.find()
        
        leagues = []
        
        for result in results:
            leagues.append(LeagueModel.from_mongo(result))
        
        return leagues

    def add_legue(self, league: LeagueModel):
        #league_dict = league.dict()
        result = self.collection.insert_one(league)
        
        return result

    def get_by_id(self, str_id):
        league = self.collection.find_one({'_id': ObjectId(str_id)})

        return LeagueModel.from_mongo(league)

    def update_league(self, league_id, league):
        league_dict = league.dict()
        return self.collection.update_one({'_id': ObjectId(league_id)}, {'$set': league_dict})

    def delete_league(self, league_id):
        return self.collection.delete_one({"_id": ObjectId(league_id)})
