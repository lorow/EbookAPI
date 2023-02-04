import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    database_testing_url: str
    environment: str

    class Config:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"
        fields = {
            "database_url": {
                "env": "DATABASE_URL",
            },
            "database_testing_url": {
                "env": "TESTING_DATABASE_URL",
            },
            "environment": {
                "env": "ENVIRONMENT",
            },
        }


config = Settings()
