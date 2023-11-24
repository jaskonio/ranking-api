from app.domain.model.person import Person


class RunnerBase(Person):
    def __init__(self, id:str='', first_name: str = '', last_name:str = '', nationality: str = '', gender: str = ''
                , photo:str = '', photo_url: str = '',  dorsal:int = 0, club: str = 'Redolat Team'
                , category: str = '') -> None:
        super().__init__(id, first_name, last_name, nationality, gender, photo, photo_url)
        self.dorsal = dorsal
        self.club = club
        self.category = category

    def __eq__(self, other):
        if self.id == other.id:
            return True

        return False
