FROM python:3.11.9-slim

WORKDIR /usr/src/app

RUN mkdir app

COPY requirements.txt ./app
COPY log_conf.yaml ./app

RUN pip install --no-cache-dir -r app/requirements.txt
RUN rm app/requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "app/log_conf.yaml"]
