import pytest


@pytest.mark.asyncio
async def test_get_all_books(local_book_repository, raw_ebook_data):
    await local_book_repository.add_book(raw_ebook_data)
    results = await local_book_repository.get_all_books()
    assert results


@pytest.mark.asyncio
async def test_get_nonexistent_book(local_book_repository):
    result = await local_book_repository.get_book("this-uuid-is-invalid")
    assert result is None


@pytest.mark.asyncio
async def test_get_get_book(local_book_repository):
    # TODO this test is broken, I need to add this data before querying for it
    result = await local_book_repository.get_book(
        "71ca726e-4330-4cb4-b761-36502eaf2010"
    )
    assert result


@pytest.mark.asyncio
async def test_add_book(local_book_repository, raw_ebook_data):
    result = await local_book_repository.add_book(raw_ebook_data)
    assert result


@pytest.mark.asyncio
async def test_remove_book(local_book_repository):
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
    await local_book_repository.add_book(book_data)
    result = await local_book_repository.remove_book(uuid)
    assert result
