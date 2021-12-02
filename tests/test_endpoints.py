import fastapi.testclient
from .fixtures import *


def test_list_all_books(test_client: fastapi.testclient.TestClient):
    response = test_client.get("/books")

    assert response.status_code == 200
    assert len(response.json())


def test_get_page_existing_book_first_page(test_client):
    response = test_client.get("/books/adduuidhere/12")
    json = response.json()

    assert response.status_code == 200
    assert json

    assert json.get("text") == "some_text"


def test_get_page_no_book_exist(test_client):
    with pytest.raises(fastapi.HTTPException):
        test_client.get("/books/adduuidhere/12")


def test_get_page_no_page(test_client):
    with pytest.raises(fastapi.HTTPException):
        test_client.get("/books/adduuidhere/999999")
