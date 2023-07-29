from app.infrastructure.mongoDB.model.runner_model import RunnerModel


class RunnerRaceDetailModel(RunnerModel):
    position: int = 0
    finished: bool = False
    is_disqualified: bool = False

    # "%H:%M:%S"
    official_time: str = ''
    official_pos: str = ''
    official_avg_time: str = ''
    official_cat_pos: str = ''
    official_gen_pos: str = ''

    # "%H:%M:%S"
    real_time: str = ''
    real_pos: str = ''
    real_avg_time: str = ''
    real_cat_pos: str = ''
    real_gen_pos: str = ''
