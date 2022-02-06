import pytest
from .fixtures import *


@pytest.mark.asyncio
async def test_get_all_books(test_local_book_repository):
    results = await test_local_book_repository.get_all_books()
    assert results


@pytest.mark.asyncio
async def test_get_nonexistent_book(test_local_book_repository):
    result = await test_local_book_repository.get_book("this-uuid-is-invalid")
    assert result is None


@pytest.mark.asyncio
async def test_get_get_book(test_local_book_repository):
    result = await test_local_book_repository.get_book("71ca726e-4330-4cb4-b761-36502eaf2010")
    assert result

@pytest.mark.asyncio
async def test_add_book(test_local_book_repository):
    book_data = {
        "uuid": "c288fa07-1ea2-4668-8f21-9537204d7a82",
        "title": "test book",
        "thumbnail": "",
        "pages": 0,
        "locations": 30000,
        "file_format": "epub",
        "file_path": "",
    }

    result = await test_local_book_repository.add_book(book_data)
    assert result


@pytest.mark.asyncio
async def test_remove_book(test_local_book_repository):
    uuid = "f47709e9-1c95-43a9-af5d-7182efc95268"

    book_data = {
        "uuid": uuid,
        "title": "test book for deletion",
        "thumbnail": "",
        "pages": 0,
        "locations": 20000,
        "file_format": "pdf",
        "file_path": "",
    }
    await test_local_book_repository.add_book(book_data)
    result = await test_local_book_repository.remove_book(uuid)
    assert result
