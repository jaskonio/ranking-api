from Infrastructure.MongoDB.MongoDBSession import get_database
from Model.LeagueModel import LeagueModel
from bson import ObjectId

class LeagueList:
    def __init__(self):
        collection_name = "LeagueList"
        self.db = get_database()
        self.collection = self.db[collection_name]  # Obtener la colección

    def add_legue(self, league: LeagueModel):
        league_dict = league.dict()
        result = self.collection.insert_one(league_dict)
        
        return result

    def get_legue_by_id(self, str_id):
        return self.collection.find_one({'_id': ObjectId(str_id)})

    def update_league(self, league_id, league):
        league_dict = league.dict()
        return self.collection.update_one({'_id': ObjectId(league_id)}, {'$set': league_dict})

    def delete_league(self, league_id):
        self.collection.delete_one({"_id": ObjectId(league_id)})  # Eliminar la race de la colección

    def close_connection(self):
        self.client.close()  # Cerrar la conexión con MongoDB
