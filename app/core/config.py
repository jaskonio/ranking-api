import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "Ranking UI"
    PROJECT_VERSION: str = "1.0.0"

    MONGODB_HOST=os.getenv("MONGODB_HOST")
    MONGODB_NAME=os.getenv("MONGODB_NAME")
    MONGODB_USER=os.getenv("MONGODB_USER")
    MONGODB_PASSWORD=os.getenv("MONGODB_PASSWORD")
    MONGODB_PORT=os.getenv("MONGODB_PORT")
    CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STING")

    AWS_KEY: str = os.getenv("AWS_KEY")
    AWS_SECRET_KEY: str = os.getenv("AWS_SECRET_KEY")
    AWS_BUCKET_NAME: str = os.getenv("AWS_BUCKET_NAME")
    AWS_IMAGE_FOLDER: str = os.getenv("AWS_IMAGE_FOLDER")

    AUTH_SECRET_KEY: str = os.getenv("AUTH_SECRET_KEY")
    AUTH_ALGORITHM: str = os.getenv("AUTH_ALGORITHM")
    AUTH_ACCESS_TOKEN_EXPIRE_MINUTES: str = int(os.getenv("AUTH_ACCESS_TOKEN_EXPIRE_MINUTES"))
    AUTH_USER: str = os.getenv("AUTH_USER")
    AUTH_PASSWORD: str = os.getenv("AUTH_PASSWORD")

settings = Settings()
