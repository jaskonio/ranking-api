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

settings = Settings()
