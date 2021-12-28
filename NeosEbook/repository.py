from typing import Iterable, List

import databases
from sqlalchemy import text, select, insert, exists

from NeosEbook.exceptions import ReadingStateAlreadyExistsException
from NeosEbook.models import ChapterLocations, NeosBook, ReadingState
from NeosEbook.schema import NeosBookDB


class BaseRepository:
    def __init__(self, db: databases.Database):
        self.db: databases.Database = db


class LocalBookRepository(BaseRepository):
    async def get_all_books(self) -> List[NeosBookDB]:
        query = select(NeosBook)
        return await self.db.fetch_all(query)

    async def get_book(self, uuid: str) -> NeosBookDB:
        query = select(NeosBook).where(text(f"uuid=='{uuid}'"))
        return await self.db.fetch_one(query)

    async def add_book(self, book) -> bool:
        query = insert(NeosBook).values(book)
        return await self.db.execute(query=query)

    async def remove_book(self, uuid) -> bool:
        query = NeosBook.delete().where(text(f"uuid=='{uuid}'"))
        return await self.db.execute(query)


class ChapterLocationsRepository(BaseRepository):
    async def add_chapter_locations(self, locations_data):
        query = insert(ChapterLocations).values(locations_data)
        return await self.db.execute(query=query)


class ReadingStateRepository(BaseRepository):
    async def get_reading_state(self, uuid):
        query = select(ReadingState).where(text(f"uuid=='{uuid}'"))
        return await self.db.execute(query)

    async def update_reading_state(self, uuid, data):
        pass

    async def add_reading_state(self, data):
        is_reading_state_present_query = select(ReadingState).where(text(f"uuid=='{data.get('uuid')}'"))
        if await self.db.fetch_one(query=is_reading_state_present_query):
            raise ReadingStateAlreadyExistsException()

        query = insert(ReadingState).values(data)
        return await self.db.execute(query)
