from app.domain.model.runner_base import RunnerBase


def build_runners(limit):
    return [build_runner(num) for num in range(0,limit)]

def build_runner(index=1):
    return RunnerBase(
        id = str(index),
        first_name = "first_name " + str(index),
        last_name = "last_name " + str(index)
    )
