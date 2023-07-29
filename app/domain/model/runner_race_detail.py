from app.domain.model.runner import Runner


class RunnerRaceDetail(Runner):
    def __init__(self, first_name: str, last_name:str = '', nationality: str = '', gender: str = ''
        , photo:str = '', photo_url: str = '',  dorsal:int = 0, club: str = 'Redolat Team'
        , category: str = '', position:int = 0, finished:bool = True, is_disqualified: bool =  False
        , official_time:str = '', official_pos:int = 0, official_avg_time:str = ''
            , official_cat_pos:int = 0, official_gen_pos:int = 0
        , real_time:str = '', real_pos:int = 0, real_avg_time:str = ''
            , real_cat_pos:int = 0, real_gen_pos:int = 0) -> None:
        super().__init__(first_name, last_name, nationality, gender, photo, photo_url, dorsal
                         , club, category)
        self.position = position
        self.finished = finished
        self.is_disqualified = is_disqualified

        # "%H:%M:%S"
        self.official_time = official_time
        self.official_pos = official_pos
        self.official_avg_time = official_avg_time
        self.official_cat_pos = official_cat_pos
        self.official_gen_pos = official_gen_pos

        # "%H:%M:%S"
        self.real_time = real_time
        self.real_pos = real_pos
        self.real_avg_time = real_avg_time
        self.real_cat_pos = real_cat_pos
        self.real_gen_pos = real_gen_pos
