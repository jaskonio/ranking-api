import csv
import requests
import json

rows = []

def add_person(row):
    url = "https://ranking-api-jpzy.onrender.com/persons"
    person = {
        "first_name": row[1],
        "last_name": row[2]
    }
    payload = json.dumps(person)

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

with open('./scripts/BASE_DE_DATOS_2023_csv.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';',)
    rows_with_header  = list(reader)
    del rows_with_header[0]
    rows = rows_with_header

print(rows)

for row in rows:
    add_person(row)

print("finish")
