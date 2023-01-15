import databases
import sqlalchemy


def get_db(config) -> databases.Database:
    return (
        databases.Database(config.database_testing_url)
        if config.environment == "TESTING"
        else databases.Database(config.database_url)
    )


metadata = sqlalchemy.MetaData()
