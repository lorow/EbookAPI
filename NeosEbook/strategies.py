import abc
import os
from typing import Type
import ebooklib
from ebooklib import epub
from NeosEbook.schema import NeosBookDB
from NeosEbook import exceptions


class BaseBookStrategy(abc.ABC):
    def __init__(self, book: NeosBookDB):
        self.book = book

    async def get_menu(self):
        raise NotImplementedError

    async def get_page(self, number) -> dict:
        raise NotImplementedError


class EPUBBookStrategy(BaseBookStrategy):

    def __init__(self, book):
        super(EPUBBookStrategy, self).__init__(book)

    async def get_menu(self):
        pass

    async def get_page(self, number):
        pass


async def get_ebook_processing_strategy(book: NeosBookDB) -> Type[BaseBookStrategy]:
    strategy_map = {"epub": EPUBBookStrategy}

    strategy = strategy_map.get(book.file_format, None)

    if not strategy:
        raise exceptions.StrategyNotImplementedException()

    return strategy
