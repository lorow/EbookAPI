from ..exceptions import StrategyNotImplementedException
from ..strategies import EPUBBookStrategy, get_ebook_processing_strategy
from .fixtures import *


@pytest.mark.asyncio
async def test_get_ebook_processing_strategy(test_epub_book):
    strategy = await get_ebook_processing_strategy(test_epub_book)
    assert strategy is not None
    assert isinstance(strategy, EPUBBookStrategy)


@pytest.mark.asyncio
async def test_get_ebook_processing_strategy_bad_extension(test_bad_extension_book):

    with pytest.raises(StrategyNotImplementedException):
        await get_ebook_processing_strategy(test_bad_extension_book)
