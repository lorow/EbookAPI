from typing import Iterable, Optional

import fastapi.exceptions

from NeosEbook.repository import (
    ChapterLocationsRepository,
    LocalBookRepository,
    ReadingStateRepository,
    BookmarkRepository,
)
from NeosEbook.schema import NeosBookDB, BookmarkSerializerModel
from NeosEbook.strategies.books import get_ebook_processing_strategy


class NeosEbookService:
    def __init__(self, db):
        self.book_repository = LocalBookRepository(db)
        self.chapters_repository = ChapterLocationsRepository(db)
        self.reading_state_repository = ReadingStateRepository(db)
        self.bookmark_repository = BookmarkRepository(db)

    async def get_books(self, q: Optional[str] = None) -> Iterable[NeosBookDB]:
        # TODO add filtering
        return await self.book_repository.get_all_books()

    async def get_page(self, book_uuid: str, page_number: Optional[int], bookmark_uuid: Optional[str]) -> dict:
        if all([page_number, bookmark_uuid]):
            raise fastapi.HTTPException(
                status_code=403, detail="Provide only the page number or the bookmark you want to access"
            )

        book = await self.book_repository.get_book(uuid=book_uuid)
        if not book:
            raise fastapi.HTTPException(
                status_code=404, detail="book with given uuid does not exist"
            )

        parser_strategy = await get_ebook_processing_strategy(book.file_format)
        parser = parser_strategy(book=book, ebook_file_path=book.file_path)

        reading_state = await self.reading_state_repository.get_reading_state(book_uuid)

        bookmark = await self.bookmark_repository.get_bookmark(bookmark_uuid=bookmark_uuid)
        if bookmark:
            page_number = bookmark.location.locations_min

        if not page_number:
            page_number = reading_state.page if book.pages else reading_state.location

        page = await parser.get_page(
            page_number, self.chapters_repository, reading_state
        )

        await self._update_reading_state(book, book.uuid, page_number)

        return page

    async def get_cover(self, book_uuid: str, output_format: str) -> bytearray:
        book = await self.book_repository.get_book(book_uuid)
        if not book:
            raise fastapi.HTTPException(
                status_code=404, detail="book with given uuid does not exist"
            )

        parser_strategy = await get_ebook_processing_strategy(book.file_format)
        parser = parser_strategy(book=book, ebook_file_path=book.file_path)
        cover = await parser.get_cover(format=output_format)

        return cover

    async def add_book_from_path(self, book_path: str):
        """Add book and index its chapters if necessary"""

        file_extension = book_path.split(".")[-1]
        parser_strategy = await get_ebook_processing_strategy(file_extension)
        parser = parser_strategy(ebook_file_path=book_path)

        book_data = await parser.get_book_data(book_path)
        book_uuid = book_data.get("uuid")

        reading_state_data = {
            "uuid": book_uuid,
            "location": 0,
            "page": 0,
            "progress": 0,
            "font_size": 14,
        }

        locations_data = None
        if not book_data.get("pages", 0):
            locations_data = await parser.get_locations_data(book_uuid)
            book_data.update({"locations": locations_data.get("total", 0)})

        await self.book_repository.add_book(book_data)
        await self.reading_state_repository.add_reading_state(reading_state_data)

        if locations_data:
            await self.chapters_repository.add_chapter_locations(
                locations_data.get("per_chapter", [])
            )

    async def add_bookmark(self, book_uuid, bookmark: BookmarkSerializerModel):
        return await self.bookmark_repository.add_bookmark(book_uuid, bookmark)

    async def remove_bookmark(self, bookmark_uuid):
        return await self.bookmark_repository.remove_bookmark(bookmark_uuid)

    async def _update_reading_state(self, book, uuid, page_number):
        reading_state_data = {}

        if book.pages:
            reading_state_data["page"] = page_number
            reading_state_data["progress"] = int((page_number / book.pages) * 100)
        if book.locations:
            reading_state_data["location"] = page_number
            reading_state_data["progress"] = int((page_number / book.locations) * 100)

        await self.reading_state_repository.update_reading_state(
            uuid, reading_state_data
        )
