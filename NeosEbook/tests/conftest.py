import pytest
from fastapi.testclient import TestClient
from ..app import app
from NeosEbook.schema import NeosBookDB
from ..database import get_db
from ..repository import LocalBookRepository
from ..settings import config


@pytest.fixture(scope="session")
def test_client():
    return TestClient(app)


@pytest.fixture()
def raw_ebook_data():
    return {
        "uuid": "c288fa07-1ea2-4668-8f21-9537204d7a82",
        "title": "test book",
        "thumbnail": "",
        "pages": 0,
        "locations": 30000,
        "file_format": "epub",
        "file_path": "",
    }


@pytest.fixture(scope="session")
def epub_book():
    return NeosBookDB(
        id=0,
        uuid="f4ed2488-5eb0-11ec-bf63-0242ac130002",
        title="some test book",
        thumbnail="None.jpg",
        current_page=12,
        locations=0,
        pages=200,
        file_format="epub",
        file_path="none.epub",
    )


@pytest.fixture(scope="session")
def bad_extension_book():
    return NeosBookDB(
        id=0,
        uuid="f4ed2488-5eb0-11ec-bf63-0242ac130002",
        title="some test book",
        thumbnail="None.jpg",
        current_page=12,
        locations=0,
        pages=200,
        file_format="notAnBookExtension",
        file_path="none.epub",
    )


@pytest.fixture
def local_book_repository():
    config.environment = "TESTING"
    db = get_db(config)
    return LocalBookRepository(db)
