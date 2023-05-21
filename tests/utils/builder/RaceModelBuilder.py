from app.model.RaceModel import RaceModel


class RaceModelBuilder:
    def create_race_moldel_fake(self, index=1, ranking=[]):
        data = {
            "name": "Race Name {}".format(index),
            "url": "Race url {}".format(index),
            "order": index,
            "ranking": ranking
        }
        return RaceModel(**dict(data))

    def create_races_model_fake(self, limit_races:int):
        races = []
        for i in range(0, limit_races):
            races.append(self.create_race_moldel_fake(index=i))
        return races
