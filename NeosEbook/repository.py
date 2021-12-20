from typing import Iterable, List

import databases
from sqlalchemy import text

from NeosEbook.models import NeosBook
from NeosEbook.schema import NeosBookDB


class LocalBookRepository:
    def __init__(self, db: databases.Database):
        self.db: databases.Database = db

    async def get_all_books(self) -> List[NeosBookDB]:
        query = NeosBook.select()
        return await self.db.fetch_all(query)

    async def get_book(self, uuid: str) -> NeosBookDB:
        query = NeosBook.select().where(text(f"uuid=='{uuid}'"))
        return await self.db.fetch_one(query)

    async def add_book(self, book) -> bool:
        pass

    async def remove_book(self, uuid) -> bool:
        pass
