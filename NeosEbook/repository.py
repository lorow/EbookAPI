from typing import Iterable

import databases

from NeosEbook.models import NeosBook
from NeosEbook.schema import NeosBookDB


class LocalBookRepository:
    def __init__(self, db: databases.Database):
        self.db: databases.Database = db

    async def get_all_books(self) -> Iterable[NeosBookDB]:
        query = NeosBook.select()
        return await self.db.fetch_all(query)

    async def get_book(self, uuid: str) -> NeosBookDB:
        query = NeosBook.select(uuid=uuid)
        return await self.db.fetch_one(query)

    async def add_book(self, book) -> bool:
        pass

    async def remove_book(self, uuid) -> bool:
        pass
