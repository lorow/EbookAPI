from typing import Iterable, Optional

import fastapi.exceptions

from NeosEbook.repository import LocalBookRepository
from NeosEbook.schema import NeosBookDB
from NeosEbook.strategies import get_ebook_processing_strategy


class NeosEbookService:
    def __init__(self, db):
        self.repository = LocalBookRepository(db)

    async def get_books(self, q: Optional[str] = None) -> Iterable[NeosBookDB]:
        return await self.repository.get_all_books()

    async def get_page(self, book_uuid, page_number) -> dict:
        book = await self.repository.get_book(uuid=book_uuid)
        if not book:
            raise fastapi.exceptions.ValidationError("book with given uuid does not exist")

        parser_strategy = get_ebook_processing_strategy(book)
        page = parser_strategy.get_page(page_number)

        return page
