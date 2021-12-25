from typing import Iterable, List

import databases
from sqlalchemy import text

from NeosEbook.models import ChapterLocations, NeosBook
from NeosEbook.schema import NeosBookDB


class BaseRepository:
    def __init__(self, db: databases.Database):
        self.db: databases.Database = db


class LocalBookRepository(BaseRepository):
    async def get_all_books(self) -> List[NeosBookDB]:
        query = NeosBook.select()
        return await self.db.fetch_all(query)

    async def get_book(self, uuid: str) -> NeosBookDB:
        query = NeosBook.select().where(text(f"uuid=='{uuid}'"))
        return await self.db.fetch_one(query)

    async def add_book(self, book) -> bool:
        query = NeosBook.insert()
        return await self.db.execute(query=query, values=book)

    async def remove_book(self, uuid) -> bool:
        query = NeosBook.delete().where(text(f"uuid=='{uuid}'"))
        return await self.db.execute(query)


class ChapterLocationsRepository(BaseRepository):
    async def add_chapter_locations(self, locations_data):
        query = ChapterLocations.insert()
        return await self.db.execute_many(query=query, values=locations_data)
