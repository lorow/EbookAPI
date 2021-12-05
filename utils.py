from dotenv import dotenv_values
import databases


def get_config() -> dict:
    config = dotenv_values()
    return config


def get_db() -> databases.Database:
    db = databases.Database(get_config().get("DATABASE_URL"))
    return db
