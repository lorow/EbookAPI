from ..exceptions import StrategyNotImplementedException
from ..strategies import EPUBBookStrategy, get_ebook_processing_strategy
from .fixtures import *


@pytest.mark.asyncio
async def test_get_ebook_processing_strategy(test_epub_book: NeosBookDB):
    strategy = await get_ebook_processing_strategy(test_epub_book.file_format)
    assert strategy is not None
    assert issubclass(strategy, EPUBBookStrategy)


@pytest.mark.asyncio
async def test_get_ebook_processing_strategy_bad_extension(test_bad_extension_book: NeosBookDB):

    with pytest.raises(StrategyNotImplementedException):
        await get_ebook_processing_strategy(test_bad_extension_book.file_format)
