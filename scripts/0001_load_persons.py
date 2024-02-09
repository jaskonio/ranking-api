import csv
import json
import requests

PERSON_ENDPOINT = "http://localhost:8000/persons"

if __name__ == '__main__':
    rows = []

    with open('./scripts/resources/2023/BASE_DE_DATOS.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';',)
        rows_with_header  = list(reader)
        del rows_with_header[0]
        rows = rows_with_header

    print("Se van a insertar " + str(len(rows)) + " nuevas personas")

    persons = []

    for row in rows:
        person = {
            "first_name": row[1],
            "last_name": row[2]
        }

        persons.append(person)

    payload = json.dumps(persons)

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", PERSON_ENDPOINT, headers=headers, data=payload, timeout=60)
    print(response.text)

    print("finish")
