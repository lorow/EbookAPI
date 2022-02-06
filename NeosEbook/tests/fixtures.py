import pytest
from fastapi.testclient import TestClient
from ..app import app
from NeosEbook.schema import NeosBookDB
from ..database import get_db
from ..repository import LocalBookRepository


@pytest.fixture(scope="session")
def test_client():
    return TestClient(app)


@pytest.fixture(scope="session")
def test_epub_book():
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
def test_bad_extension_book():
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


@pytest.fixture(scope="session")
def test_local_book_repository():
    db = get_db()
    return LocalBookRepository(db)
