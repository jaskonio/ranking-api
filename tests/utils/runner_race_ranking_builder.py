from app.domain.model.runner_race_ranking import RunnerRaceRanking

class RunnerRaceRankingBuilder:
    def __init__(self):
        self.id = '1'
        self.first_name = 'John'
        self.last_name = 'Doe'
        self.nationality = 'US'
        self.gender = 'Male'
        self.photo = 'base64encodedphoto'
        self.photo_url = '/person/image/1'
        self.dorsal = 123
        self.club = 'Redolat Team'
        self.category = 'Senior'
        self.position = 1
        self.finished = True
        self.is_disqualified = False
        self.official_time = '00:30:00'
        self.official_pos = 1
        self.official_avg_time = '05:00 / km'
        self.official_cat_pos = 1
        self.official_gen_pos = 1
        self.real_time = '00:28:00'
        self.real_pos = 1
        self.real_avg_time = '04:40 / km'
        self.real_cat_pos = 1
        self.real_gen_pos = 1
        self.points = 25.0
        self.posiciones_ant = [1, 2, 3]
        self.averages_ant = ['04:50 / km', '05:00 / km', '04:45 / km']
        self.position_general_ant = [1, 2, 3]

    def with_id(self, id):
        self.id = id
        return self

    def with_name(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        return self

    def with_nationality(self, nationality):
        self.nationality = nationality
        return self

    def with_gender(self, gender):
        self.gender = gender
        return self

    def with_photo(self, photo):
        self.photo = photo
        return self

    def with_photo_url(self, photo_url):
        self.photo_url = photo_url
        return self

    def with_dorsal(self, dorsal):
        self.dorsal = dorsal
        return self

    def with_club(self, club):
        self.club = club
        return self

    def with_category(self, category):
        self.category = category
        return self

    def with_position(self, position):
        self.position = position
        return self

    def with_finished(self, finished):
        self.finished = finished
        return self

    def with_is_disqualified(self, is_disqualified):
        self.is_disqualified = is_disqualified
        return self

    def with_official_time(self, official_time):
        self.official_time = official_time
        return self

    def with_official_pos(self, official_pos):
        self.official_pos = official_pos
        return self

    def with_official_avg_time(self, official_avg_time):
        self.official_avg_time = official_avg_time
        return self

    def with_official_cat_pos(self, official_cat_pos):
        self.official_cat_pos = official_cat_pos
        return self

    def with_official_gen_pos(self, official_gen_pos):
        self.official_gen_pos = official_gen_pos
        return self

    def with_real_time(self, real_time):
        self.real_time = real_time
        return self

    def with_real_pos(self, real_pos):
        self.real_pos = real_pos
        return self

    def with_real_avg_time(self, real_avg_time):
        self.real_avg_time = real_avg_time
        return self

    def with_real_cat_pos(self, real_cat_pos):
        self.real_cat_pos = real_cat_pos
        return self

    def with_real_gen_pos(self, real_gen_pos):
        self.real_gen_pos = real_gen_pos
        return self

    def with_points(self, points):
        self.points = points
        return self

    def with_posiciones_ant(self, posiciones_ant):
        self.posiciones_ant = posiciones_ant
        return self

    def with_averages_ant(self, averages_ant):
        self.averages_ant = averages_ant
        return self

    def with_position_general_ant(self, position_general_ant):
        self.position_general_ant = position_general_ant
        return self

    def build(self):
        return RunnerRaceRanking(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            nationality=self.nationality,
            gender=self.gender,
            photo=self.photo,
            photo_url=self.photo_url,
            dorsal=self.dorsal,
            club=self.club,
            category=self.category,
            position=self.position,
            finished=self.finished,
            is_disqualified=self.is_disqualified,
            official_time=self.official_time,
            official_pos=self.official_pos,
            official_avg_time=self.official_avg_time,
            official_cat_pos=self.official_cat_pos,
            official_gen_pos=self.official_gen_pos,
            real_time=self.real_time,
            real_pos=self.real_pos,
            real_avg_time=self.real_avg_time,
            real_cat_pos=self.real_cat_pos,
            real_gen_pos=self.real_gen_pos,
            points=self.points,
            posiciones_ant=self.posiciones_ant,
            averages_ant=self.averages_ant,
            position_general_ant=self.position_general_ant
        )
