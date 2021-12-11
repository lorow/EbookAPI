from typing import Iterable, Optional

from NeosEbook.repository import LocalBookRepository
from NeosEbook.schema import NeosBookDB


class NeosEbookService:
    def __init__(self, db):
        self.repository = LocalBookRepository(db)

    async def get_books(self, q: Optional[str] = None) -> Iterable[NeosBookDB]:
        return await self.repository.get_all_books()

    async def get_page(self, book_uuid, page_number) -> dict:
        pass