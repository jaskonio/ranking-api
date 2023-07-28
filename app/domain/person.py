class Person():

    def __init__(self, first_name: str, last_name:str = '', nationality: str = '',
                 gender: str = '', photo:str = '', photo_url: str = '') -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.nationality = nationality
        self.gender = gender
        self.photo = photo
        self.photo_url = photo_url
