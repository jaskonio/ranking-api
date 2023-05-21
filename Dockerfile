FROM python:3.8.10

WORKDIR /usr/src/app

RUN mkdir app

COPY requirements.txt ./app
COPY log_conf.yaml ./app

RUN pip install --no-cache-dir -r app/requirements.txt

COPY app/ ./app/
COPY .env ./

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--log-config", "app/log_conf.yaml"]
