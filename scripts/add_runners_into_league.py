# Este script a apartir de un csv con las columnas dorsal, nombre, apellido, nombre de liga y genero 
# añade cada runner a la lista de participantes de una liga
# IMPORTANTE este script actualiza el ranking final
import csv
import requests
import json

path_file = './scripts/eliTEAM - Masculino_2023.csv'
base_path = "https://ranking-api-jpzy.onrender.com"
#base_path = "http://127.0.0.1:8000/leagues/64aa891c06cb93474117df5e/add_runner"


def get_league_by_name(league_name):
    url = base_path + "/leagues"
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)

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
    url = base_path + "/persons"
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)

    return response.json()['items']

def add_person_into_league(person_csv, league, person_db):
    url = base_path + "/leagues/{}/add_runner".format(league['id'])

    dorsal = str(0) if person_csv[0] == "CaC" else person_csv[0]

    person = {
        "name": person_csv[1],
        "last_name": person_csv[2],
        "dorsal": dorsal,
        "person_id": person_db['id']
    }

    payload = json.dumps(person)

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

if __name__ == '__main__':
    persons = persons_from_file(path_file)
    current_league_name = persons[0][3]

    league = get_league_by_name(current_league_name)

    if league is None:
        print("La liga {} no se ha encontrado.".format(current_league_name))

    all_person = get_all_person()
    for person in persons:
        person_db = list(filter(lambda current_person: current_person['first_name'] + ' ' + current_person['last_name'] == person[1] + ' ' + person[2], all_person))

        if len(person_db) == 0:
            print("No se ha encontrado a la person {} {}".format(person[1], person[2]))
            continue

        add_person_into_league(person, league, person_db[0])

print("finish")
