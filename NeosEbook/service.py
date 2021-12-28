from typing import Iterable, Optional

import fastapi.exceptions

from NeosEbook.repository import ChapterLocationsRepository, LocalBookRepository
from NeosEbook.schema import NeosBookDB
from NeosEbook.strategies import get_ebook_processing_strategy


class NeosEbookService:
    def __init__(self, db):
        self.book_repository = LocalBookRepository(db)
        self.chapters_repository = ChapterLocationsRepository(db)

    async def get_books(self, q: Optional[str] = None) -> Iterable[NeosBookDB]:
        return await self.book_repository.get_all_books()

    async def get_page(self, book_uuid: str, page_number: Optional[int]) -> dict:
        book = await self.book_repository.get_book(uuid=book_uuid)
        if not book:
            raise fastapi.HTTPException(status_code=404, detail="book with given uuid does not exist")

        book = NeosBookDB(**book)

        parser_strategy = await get_ebook_processing_strategy(book.file_format)
        parser = parser_strategy(book=book, ebook_file_path=book.file_path)
        page = await parser.get_page(page_number)

        return page

    async def get_cover(self, book_uuid) -> bytearray:
        book = await self.book_repository.get_book(book_uuid)

        parser_strategy = await get_ebook_processing_strategy(book.file_format)
        parser = parser_strategy(book=book, ebook_file_path=book.file_path)
        cover = await parser.get_cover()

        return cover

    async def add_book_from_path(self, book_path: str):
        """Add book and index its chapters if necessary"""

        file_extension = book_path.split(".")[-1]
        parser_strategy = await get_ebook_processing_strategy(file_extension)
        parser = parser_strategy(ebook_file_path=book_path)

        book_data = await parser.get_book_data(book_path)

        locations_data = None
        if not book_data.get("pages", 0):
            locations_data = await parser.get_locations_data(book_data.get("uuid"))
            book_data.update({"locations": locations_data.get("total", 0)})

        await self.book_repository.add_book(book_data)

        if locations_data:
            await self.chapters_repository.add_chapter_locations(locations_data.get("per_chapter", []))
