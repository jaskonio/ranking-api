# ranking-api

### Prepare virual environment
```cmd
python3 -m  venv env
source env/bin/activate
pip3 install -r requirements.txt
```


# Development
```cmd
 uvicorn main:app --reload
```


# Docker
## Build 

```cmd
    docker build -t ranking-api:latest .
```


## Run 

```cmd
    docker run -d --rm --name ranking-api -p 9000:8080 ranking-api:latest
```