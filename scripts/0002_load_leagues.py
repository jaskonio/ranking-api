import json
import requests

LEAGUE_ENDPOINT = "http://localhost:8000/leagues/"
LEAGUES_NAMES = ["eliTEAM - Masculino", "paqueliTEAM - Masculino"]

if __name__ == '__main__':
    print("Se van a insertar " + str(len(LEAGUES_NAMES)) + " nuevas ligas")

    leagues = []

    for league_name in LEAGUES_NAMES:
        league = {
            "name": league_name
        }

        leagues.append(league)

    payload = json.dumps(leagues)

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", LEAGUE_ENDPOINT, headers=headers, data=payload, timeout=60)
    print(response.text)

    print("finish")
