import fastapi.testclient


def test_list_all_books(test_client: fastapi.testclient.TestClient):
    response = test_client.get("/books")

    assert response.status_code == 200
    assert len(response.json())


def test_get_page_existing_book_first_page(test_client):
    response = test_client.get(
        "/books/71ca726e-4330-4cb4-b761-36502eaf2010/page/?page=0"
    )
    json = response.json()

    assert response.status_code == 200
    assert json


def test_get_page_no_book_exist(test_client):
    response = test_client.get(
        "/books/f4ed2488-5eb0-11ec-bf63-0242ac130002/page/?page=12"
    )
    assert response.status_code == 404


def test_get_page_no_page(test_client):
    response = test_client.get(
        "/books/f4ed2488-5eb0-11ec-bf63-0242ac130002/page/?page=9999999"
    )
    assert response.status_code == 404


def test_get_cover_for_book_not_book_exists(test_client):
    response = test_client.get("/books/f4ed2488-5eb0-11ec-bf63-0242ac130002/cover")
    assert response.status_code == 404


def test_get_cover_for_existing_book(test_client):
    response = test_client.get("/books/71ca726e-4330-4cb4-b761-36502eaf2010/cover")
    assert response.status_code == 200
