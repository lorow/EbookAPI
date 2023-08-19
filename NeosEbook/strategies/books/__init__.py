from typing import Type

from .Epub import EPUBBookStrategy
from .base import BaseBookStrategy
from NeosEbook import exceptions


__strategy_map = {"epub": EPUBBookStrategy}
async def get_ebook_processing_strategy(file_extension: str) -> Type[BaseBookStrategy]:
    if strategy := __strategy_map.get(file_extension):
        return strategy
    raise exceptions.StrategyNotImplementedException()
