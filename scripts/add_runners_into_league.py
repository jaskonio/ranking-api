# Este script a apartir de un csv con las columnas dorsal, nombre, apellido, nombre de liga y genero
# añade cada runner a la lista de participantes de una liga
# IMPORTANTE este script actualiza el ranking final
import csv
import json
from requests import request


PATH_FILE = './scripts/eliTEAM - Masculino_2023.csv'
#BASE_PATH = "https://ranking-api-jpzy.onrender.com"
BASE_PATH = "http://127.0.0.1:8000"


def get_league_by_name(league_name):
    url = BASE_PATH + "/leagues"
    headers = {
        'Content-Type': 'application/json'
    }

    response = request("GET", url, headers=headers, timeout=60)

    for league in response.json():
        if league['name'] == league_name:
            return league

    return None

def persons_from_file(path_file):
    with open(path_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';',)
        rows_with_header  = list(reader)
        del rows_with_header[0]
        return rows_with_header

def get_all_person():
    url = BASE_PATH + "/persons"
    headers = {
        'Content-Type': 'application/json'
    }

    response = request("GET", url, headers=headers, timeout=60)

    return response.json()

def add_person_into_league(person_csv, league, person_db):
    league_id = league['id']

    url = BASE_PATH + f'/leagues/{league_id}/add_runner'

    dorsal = str(0) if person_csv[0] == "CaC" else person_csv[0]

    person = {
        "first_name": person_db['first_name'],
        "last_name": person_db['last_name'],
        "nationality": person_db['nationality'],
        "gender": person_db['gender'],
        "photo": person_db['photo'],
        "photo_url": person_db['photo_url'],
        "dorsal": dorsal,
        "club": 'Redolat Team',
        "category": ''
    }

    payload = json.dumps(person)

    headers = {
        'Content-Type': 'application/json'
    }

    request("POST", url, headers=headers, data=payload, timeout=60)

    print("[INFO] finish request")

if __name__ == '__main__':
    persons = persons_from_file(PATH_FILE)
    current_league_name = persons[0][3]

    print("[INFO] Getting league")
    league = get_league_by_name(current_league_name)

    if league is None:
        print("La liga %s no se ha encontrado.", str(current_league_name))

    print("[INFO] Getting all persons")
    all_person = get_all_person()

    for person in persons:
        person_db = list(filter(lambda current_person: current_person['first_name'] + ' ' + current_person['last_name'] == person[1] + ' ' + person[2], all_person))

        if len(person_db) == 0:
            print("No se ha encontrado a la persona %s %s", str(person[1]), str(person[2]))
            continue

        print("[INFO] Start add person")
        add_person_into_league(person, league, person_db[0])
        print("[INFO] End add person")

print("finish")
