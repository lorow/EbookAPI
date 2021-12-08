import databases

from NeosEbook.settings import Settings


async def get_db() -> databases.Database:
    config = Settings()

    if config.environment == "TESTING":
        db = databases.Database(config.database_testing_url)
    else:
        db = databases.Database(config.database_url)
    return db
