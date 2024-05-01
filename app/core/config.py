import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "Ranking Redolat Team"
    PROJECT_VERSION: str = "1.0.0"

    DATABASE_TYPE: str = os.getenv("DATABASE_TYPE")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    CONNECTION_STRING: str = ''

    if DATABASE_TYPE == 'MONGODB':
        CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STING")

    AWS_KEY: str = os.getenv("AWS_KEY")
    AWS_SECRET_KEY: str = os.getenv("AWS_SECRET_KEY")
    AWS_BUCKET_NAME: str = os.getenv("AWS_BUCKET_NAME")
    AWS_IMAGE_FOLDER: str = os.getenv("AWS_IMAGE_FOLDER")

settings = Settings()
