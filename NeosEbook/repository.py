from typing import Iterable

import databases

from NeosEbook.schema import NeosBookDB


class LocalBookRepository:
    def __init__(self, db: databases.Database):
        self.db: databases.Database = db

    async def get_all_books(self) -> Iterable[NeosBookDB]:
        pass

    async def get_book(self, uuid: str) -> NeosBookDB:
        pass

    async def add_book(self, book) -> bool:
        pass

    async def remove_book(self, uuid) -> bool:
        pass
