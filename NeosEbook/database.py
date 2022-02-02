import databases
import sqlalchemy

from NeosEbook.settings import Settings


def get_db() -> databases.Database:
    config = Settings()

    return (
        databases.Database(config.database_testing_url)
        if config.environment == "TESTING"
        else databases.Database(config.database_url)
    )


db = get_db()
metadata = sqlalchemy.MetaData()
