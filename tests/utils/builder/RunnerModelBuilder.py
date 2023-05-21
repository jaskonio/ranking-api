from app.model.RunnerModel import RunnerModel


class RunnerModelBuilder:
    def create_runner_model_fake(self, dorsal=1):

        data = {
            "dorsal": dorsal,
            "name": "Runner fake {}".format(dorsal)
        }
        return RunnerModel(**dict(data))

    def create_runners_model_fake(self, number:int):
        runners = []
        for i in range(1, number+1):
            runners.append(self.create_runner_model_fake(i))
        return runners