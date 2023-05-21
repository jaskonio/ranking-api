from app.model.RunnerBaseModel import RunnerBaseModel


class RunnerBaseModelBuilder:
    def create_new_runner_base_fake(self, dorsal=1):
        runner = {
            "dorsal": dorsal,
            "name": "Runner {}".format(dorsal)
        }
        new_runner = RunnerBaseModel(**dict(runner))
        
        return new_runner

    def create_runners_base_fake(self, limit=2):
        runners = []
        
        for i in range(1, limit+1):
            runners.append(self.create_new_runner_base_fake(i))
        return runners