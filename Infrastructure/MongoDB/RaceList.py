from ast import List
from Domain.Race import Race
from pymongo import MongoClient
import os
from fastapi.encoders import jsonable_encoder

class RaceList:
    def __init__(self):
        MONGODB_URI = os.getenv('MONGODB_URI')
        MONGODB_DATABASE = os.getenv('MONGODB_DATABASE')
        collection_name = "raceLists"

        self.client = MongoClient(MONGODB_URI)  # Establecer conexión con el cliente de MongoDB
        self.db = self.client[MONGODB_DATABASE]  # Obtener la base de datos
        self.collection = self.db[collection_name]  # Obtener la colección

    def add_race(self, race: Race):
        print("Se procede a guarda la carrera")
        race_obj = jsonable_encoder(race)

        self.collection.insert_one(race_obj)  # Insertar el objeto race en la colección

    def get_races(self):
        races:List[Race] = list()

        for data in self.collection.find():
            race = Race(data['name'])  # Crear un nuevo objeto race con los datos de MongoDB
            race.ranking = data['ranking']  # Restaurar el ranking de la race
            race.order = data['order']
            race.sorted = data['sorted']

            races.append(race)

        return races

    def update_carrera(self, race):
        self.collection.update_one({"name": race.name}, {"$set": race.__dict__})  # Actualizar la carrera en MongoDB

    def delete_race(self, race: Race):
        self.collection.delete_one({"name": race.name})  # Eliminar la race de la colección

    def clear_races(self):
        self.collection.delete_many({})  # Eliminar todas las races de la colección

    def close_connection(self):
        self.client.close()  # Cerrar la conexión con MongoDB
