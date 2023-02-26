# ranking-api

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
    docker run --rm --name ranking-api -p 9000:8080 ranking-api:latest
```