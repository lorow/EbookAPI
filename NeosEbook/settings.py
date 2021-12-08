from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    database_testing_url: str
    environment: str

    class Config:
        prefix = "neos__"
