import abc

from NeosEbook.schema import NeosBookBase
from NeosEbook import exceptions


class BaseBookStrategy(abc.ABC):
    def __init__(self, book: NeosBookBase):
        self.book = book

    def get_page(self, number) -> dict:
        pass


class EPUBBookStrategy:
    def get_page(self, number):
        pass


def get_ebook_processing_strategy(book: NeosBookBase) -> BaseBookStrategy:
    strategy_map = {"epub": EPUBBookStrategy}

    strategy = strategy_map.get(book.file_format, None)

    if not strategy:
        raise exceptions.StrategyNotImplementedException()

    return strategy
