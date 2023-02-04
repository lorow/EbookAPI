import pytest
from ..exceptions import StrategyNotImplementedException
from ..strategies import EPUBBookStrategy, get_ebook_processing_strategy


@pytest.mark.asyncio
async def test_get_ebook_processing_strategy(epub_book):
    strategy = await get_ebook_processing_strategy(epub_book.file_format)
    assert strategy is not None
    assert issubclass(strategy, EPUBBookStrategy)


@pytest.mark.asyncio
async def test_get_ebook_processing_strategy_bad_extension(bad_extension_book):

    with pytest.raises(StrategyNotImplementedException):
        await get_ebook_processing_strategy(bad_extension_book.file_format)
