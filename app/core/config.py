"""
TODO
"""
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    """_summary_
    """
    PROJECT_NAME: str = "Ranking Redolat Team"
    PROJECT_VERSION: str = "1.0.0"

    MONGODB_URI: str = os.getenv("MONGODB_URI")
    MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE")

    TEST_USER_EMAIL = "test@example.com"

settings = Settings()
