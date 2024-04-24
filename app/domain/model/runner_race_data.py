class RunnerRaceData():
    def __init__(self, first_name: str = '', last_name: str = '', nationality: str = '', gender: str = ''
                    , dorsal: int = 0, club: str = '' , category: str = '', finished: bool = True
                    , official_time: str = '', official_pos: int = 0, official_avg_time: str = ''
                    , official_cat_pos: int = 0, official_gen_pos: int = 0 , real_time: str = '', real_pos: int = 0, real_avg_time: str = ''
                    , real_cat_pos: int = 0, real_gen_pos: int = 0) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.nationality = nationality
        self.gender = gender
        self.dorsal = dorsal
        self.club = club
        self.category = category

        self.finished = finished

        self.official_time = official_time
        self.official_pos = official_pos
        self.official_avg_time = official_avg_time
        self.official_cat_pos = official_cat_pos
        self.official_gen_pos = official_gen_pos

        self.real_time = real_time
        self.real_pos = real_pos
        self.real_avg_time = real_avg_time
        self.real_cat_pos = real_cat_pos
        self.real_gen_pos = real_gen_pos

    def to_dict(self):
        # Si el objeto es una instancia de dict, simplemente lo devolvemos
        if isinstance(self, dict):
            return self

        # Si el objeto es una instancia de una clase personalizada, convertimos sus atributos
        if hasattr(self, '__dict__'):
            obj_dict = vars(self)

            # Convertir recursivamente los atributos que también sean objetos
            for key, value in obj_dict.items():
                if isinstance(value, (list, tuple)):
                    obj_dict[key] = [item.to_dict() if hasattr(item, '__dict__') else item for item in value]
                elif hasattr(value, '__dict__'):
                    obj_dict[key] = value.to_dict

            return obj_dict

        # Si el objeto no es una instancia de una clase personalizada, simplemente lo devolvemos
        return self
