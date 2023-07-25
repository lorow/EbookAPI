from typing import List, Optional

import databases
from sqlalchemy import between, insert, select, text

from NeosEbook.exceptions import (
    ReadingStateAlreadyExistsException,
    BookmarkAlreadyExistsException,
)
from NeosEbook import models
from NeosEbook import schema


class BaseRepository:
    def __init__(self, db: databases.Database):
        self.db: databases.Database = db


class LocalBookRepository(BaseRepository):
    async def get_all_books(self) -> List[schema.NeosBookDB]:
        query = select(models.NeosBook)
        data = await self.db.fetch_all(query)
        return list(map(lambda row: schema.NeosBookDB(**dict(row)), data))

    async def get_book(self, uuid: str) -> Optional[schema.NeosBookDB]:
        query = select(models.NeosBook).where(text(f"uuid=='{uuid}'"))
        data = await self.db.fetch_one(query)
        if data:
            return schema.NeosBookDB(**dict(data))

    async def add_book(self, book) -> bool:
        query = insert(models.NeosBook).values(book)
        return await self.db.execute(query=query)

    async def remove_book(self, uuid) -> bool:
        query = models.NeosBook.delete().where(text(f"uuid=='{uuid}'"))
        return await self.db.execute(query)


class ChapterLocationsRepository(BaseRepository):
    async def add_chapter_locations(self, locations_data):
        query = insert(models.ChapterLocations).values(locations_data)
        return await self.db.execute(query=query)

    async def get_chapter_by_location(self, uuid, location) -> models.ChapterLocations:
        query = (
            select(models.ChapterLocations)
            .where(text(f"uuid=='{uuid}'"))
            .where(
                (
                    between(
                        location,
                        models.ChapterLocations.c.locations_min,
                        models.ChapterLocations.c.locations_max,
                    )
                )
            )
        )
        data = await self.db.fetch_one(query)
        return models.ChapterLocations(**dict(data))


class ReadingStateRepository(BaseRepository):
    async def get_reading_state(self, uuid) -> schema.ReadingState:
        query = select(models.ReadingState).where(text(f"uuid=='{uuid}'"))
        data = await self.db.fetch_one(query)
        return schema.ReadingState(**dict(data))

    async def update_reading_state(self, uuid, data):
        raise NotImplementedError
        # TODO implement this

    async def add_reading_state(self, data):
        is_reading_state_present_query = select(models.ReadingState).where(
            text(f"uuid=='{data.get('uuid')}'")
        )
        if await self.db.fetch_one(query=is_reading_state_present_query):
            raise ReadingStateAlreadyExistsException()

        query = insert(models.ReadingState).values(data)
        return await self.db.execute(query)


class BookmarkRepository(BaseRepository):

    async def get_bookmark(self, bookmark_uuid: Optional[str]) -> schema.Bookmark:
        if not bookmark_uuid:
            return None

        query = select(models.Bookmark, models.ChapterLocations).join(models.ChapterLocations).where(text(f"uuid=='{bookmark_uuid}'"))
        data = await self.db.fetch_one(query)
        if data:
            location = models.ChapterLocations(**dict(data).get("ChapterLocations"))
            return schema.Bookmark(location=location)

    async def add_bookmark(
        self, book_uuid: str, bookmark: schema.BookmarkSerializerModel
    ) -> bool:
        is_bookmark_present_query = select(models.Bookmark).where(
            text(f"location_id=={bookmark.location}"), text(f"book_id=={book_uuid}")
        )

        if await self.db.fetch_one(query=is_bookmark_present_query):
            raise BookmarkAlreadyExistsException()

        query = insert(models.Bookmark).values(
            {
                "book_uuid": book_uuid,
                "location_id": bookmark.location,
            }
        )

        return await self.db.execute(query)

    async def remove_bookmark(self, bookmark_uuid: str):
        query = models.Bookmark.delete().where(text(f"uuid=={bookmark_uuid}"))
        return await self.db.execute(query)
