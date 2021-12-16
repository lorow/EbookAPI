from .fixtures import *
from ..exceptions import StrategyNotImplementedException
from ..strategies import get_ebook_processing_strategy, EPUBBookStrategy


def test_get_ebook_processing_strategy(test_epub_book):
    strategy = get_ebook_processing_strategy(test_epub_book)
    assert strategy is not None
    assert issubclass(strategy, EPUBBookStrategy)


def test_get_ebook_processing_strategy_bad_extension(test_bad_extension_book):

    with pytest.raises(StrategyNotImplementedException):
        get_ebook_processing_strategy(test_bad_extension_book)
