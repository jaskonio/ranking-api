from app.domain.model.runner_race_ranking import RunnerRaceRanking


def build_runners_race_ranking(limit):
    return [build_runner_race_ranking(num) for num in range(0, limit)]

def build_runner_race_ranking(index, finished=True):
    return RunnerRaceRanking(
        id = str(index),
        first_name = "first_name " + str(index),
        last_name = "last_name " + str(index),
        finished=finished
    )
