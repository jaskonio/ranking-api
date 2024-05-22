# Este script a apartir de un csv con las columnas dorsal, nombre, apellido, nombre de liga y genero
# añade cada runner a la lista de participantes de una liga
# IMPORTANTE este script actualiza el ranking final
import csv
import json
from typing import List
from requests import request


PATH_FILE = './scripts/resources/2023/eliTEAM - Masculino.csv'
# BASE_PATH = "https://ranking-api-jpzy.onrender.com"

BASE_PATH = "http://localhost:8000"
PERSON_ENDPOINT = BASE_PATH + "/persons"
LEAGUE_ENDPOINT = BASE_PATH + "/leagues/"
ADD_RUNNER_INTO_LEAGUE_ENDPOINT = BASE_PATH + "/leagues/$$LEAGUE_ID$$/add_runner"

class PersonFile():
    def __init__(self, first_name: str = '', last_name:str = '', dorsal: int = 0, gender:str = ''
                    ,league_name: str = '', league_id: str = ''):
        self.first_name = first_name
        self.last_name = last_name
        self.dorsal = 0 if dorsal == "CaC" else dorsal
        self.gender = gender
        self.league_name = league_name
        self.league_id = league_id

class Person():
    def __init__(self, id:str='', first_name: str = '', last_name:str = '', nationality: str = '',
                    gender: str = '', photo:str = '', photo_url: str = ''):
        self.id = str(id)
        self.first_name = first_name
        self.last_name = last_name
        self.nationality = nationality
        self.gender = gender
        self.photo = photo
        self.photo_url = photo_url

class Runner(Person):
    def __init__(self, id:str='', first_name: str = '', last_name:str = '', nationality: str = '',
                    gender: str = '', photo:str = '', photo_url: str = '', dorsal:int=0):
        super().__init__(id, first_name, last_name, nationality, gender, photo, photo_url)
        self.dorsal = dorsal

class RunnerBody():
    def __init__(self, person_id:str='', dorsal:int=0):
        self.person_id = str(person_id)
        self.dorsal = int(dorsal)

def persons_from_file(path_file):
    with open(path_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';',)
        rows_with_header  = list(reader)
        del rows_with_header[0]

        persons:List[PersonFile] = []

        for row in rows_with_header:
            person = PersonFile(first_name=row[1], last_name=row[2]
                          , dorsal=row[0], gender=row[4], league_name=row[3])
            persons.append(person)

        return persons

def get_league_by_name(league_name):
    headers = {
        'Content-Type': 'application/json'
    }

    response = request("GET", LEAGUE_ENDPOINT, headers=headers, timeout=60)

    for league in response.json():
        if league['name'] == league_name:
            return league

    return None

def get_all_person():
    headers = {
        'Content-Type': 'application/json'
    }

    response = request("GET", PERSON_ENDPOINT, headers=headers, timeout=60)

    return [Person(**item) for item in response.json()]

def add_person_into_league(person_file:PersonFile, league_id:str, person_db:Person):
    url = ADD_RUNNER_INTO_LEAGUE_ENDPOINT.replace("$$LEAGUE_ID$$", league_id)

    runner: RunnerBody = RunnerBody(person_id=person_db.id, dorsal=person_file.dorsal)

    payload = json.dumps(runner.__dict__)

    headers = {
        'Content-Type': 'application/json'
    }

    print("payload")
    print(payload)

    response = request("POST", url, headers=headers, data=payload, timeout=60)

    if response.status_code == 200:
        print("[INFO] finish request")
    else:
        print("[ERROR] Fail request")
        print(response.content)

if __name__ == '__main__':
    persons:List[PersonFile] = persons_from_file(PATH_FILE)

    current_league_name = persons[0].league_name

    print("[INFO] Getting league")
    league = get_league_by_name(current_league_name)

    if league is None:
        print("La liga %s no se ha encontrado.", str(current_league_name))

    print("[INFO] Getting all persons")
    all_person_db = get_all_person()

    for person_file in persons:
        equal_person_db:Person = Person()

        for person_db in all_person_db:
            if person_db.first_name + person_db.last_name == person_file.first_name + person_file.last_name:
                equal_person_db = person_db
                break

        if equal_person_db.id == '':
            print("No se ha encontrado a la persona %s %s", str(person_file.first_name),str(person_file.last_name))
            continue

        print("[INFO] Start add person")
        add_person_into_league(person_file, league['id'], equal_person_db)
        print("[INFO] End add person")

print("finish")
