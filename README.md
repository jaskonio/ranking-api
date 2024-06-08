# ranking-api

## Install python version

```bash
3.11.4
```

## Prepare virual environment in Linux

```cmd
python3 -m  venv env
source env/bin/activate
pip3 install -r requirements.txt
```

## Prepare virual environment in Windows

```cmd
python -m  venv env
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Development

```cmd
 uvicorn main:app --reload
```

## Docker

### Build

```cmd
    docker build -t ranking-api .
```

### Run

```cmd
    docker run -d --rm --name ranking-api -p 8000:8000 --env-file=.env ranking-api
```

### Stop

```cmd
    docker stop ranking-api
```

## Testing

Execute unittest:

```cmd
    python -m unittest discover -s tests/ -p 'test*.py' -v --locals
```

```cmd
    pytest .\tests\ --html=reports\execution\report_execution_test.html
```

## Coverage Code

First, run the coverage module to generate the coverage data:

```cmd
    coverage run -m unittest
```

Second, turn the coverage data into a report:

```cmd
    coverage report --include app\*
```

To generate the coverage report in HTML format, you change the option of the coverage module to HTML like this:

```cmd
    coverage html --include app\* -d reports\coverage
```

```cmd
    coverage run -m unittest && coverage report --include app\* && coverage html --include app\* -d reports\coverage
```

## Style

Check pylint

```cmd
    pylint ./app/
```

## Install Docker

[Guide to install docker](https://docs.docker.com/engine/install/ubuntu/)

Start/Stop mongoDB

```bash
docker start ranking-db-mongo
docker stop ranking-db-mongo
docker rm ranking-db-mongo
```

## .env Config file

```bash
APP_PORT=8000

MONGODB_HOST=xxxx
MONGODB_NAME=xxx
MONGODB_USER=admin
MONGODB_PASSWORD=admin
MONGODB_PORT=

AWS_KEY=xxxxxx
AWS_SECRET_KEY=xxxxxxxx
AWS_BUCKET_NAME=xxxxxxxx
AWS_IMAGE_FOLDER=xxxxxxxxx
```

## Use docker compose

```bash
docker volume create ranking-mongo-db
docker compose build && docker compose up -d
docker compose stop && docker compose rm -f # stop and delete
docker volume rm ranking-mongo-db

docker-compose logs -f

docker-compose stop
docker-compose start
```

Create MongoDB Container

```bash
docker run -d --name ranking-db-mongo \
-v ./data:/data/db \
-p 27017:27017 \
-e MONGO_INITDB_ROOT_USERNAME=admin \
-e MONGO_INITDB_ROOT_PASSWORD=admin \
-e MONGO_INITDB_DATABASE=rankings \
mongo:5.0.24
```

Active admin user:

```bash
docker exec -it ranking-api-mongo_db-1 bash
mongosh -u admin
use rankings
db.createUser(
    {
        user: "admin",
        pwd: "admin",
        roles: [
            {
                role: "readWrite",
                db: "rankings"
            }
        ]
    }
);
db.createCollection("test");
```

## Docker run only app

```bash
docker build -t app-ranking .
docker run --name app-ranking --env-file .env -d -p 8000:8000 app-ranking
docker logs -f app-ranking
docker stop app-ranking && docker rm app-ranking
```

## Deploy nging config

```bash
sudo cp ranking-app.com /etc/nginx/sites-available/ranking-app.com
sudo ln -s /etc/nginx/sites-available/ranking-app.com /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

## JWT

Use [jwt.io](https://jwt.io/).

Body to admin json:

Algorithm: HS256
Use AUTH_SECRET_KEY: asdas

```bash
{
  "iat": 1715787060,
  "exp": 1905089318,
  "user_name": "jonatan",
  "roles": [
    "view",
    "admin"
  ]
}
```
