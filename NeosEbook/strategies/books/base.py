import abc
from typing import Optional
from NeosEbook.schema import NeosBookDB

class BaseBookStrategy(abc.ABC):
    def __init__(self, book: Optional[NeosBookDB] = None, ebook_file_path: str = None):
        self.book = book

    async def get_menu(self):
        raise NotImplementedError

    async def get_page(self, number, chapters_repository, reading_state) -> dict:
        raise NotImplementedError

    async def get_cover(self, output_format) -> bytearray:
        raise NotImplementedError

    async def get_book_data(self, book_path: str) -> dict:
        raise NotImplementedError

    async def get_locations_data(self, book_uuid) -> dict:
        raise NotImplementedError

    @staticmethod
    async def _get_amount_of_locations_per_page_by_font_size(
        font_size: int = 14,
    ) -> int:
        page_size_x = 816
        page_size_y = 1056
        line_size = 2.5
        locations_x = (page_size_x / font_size) / 128
        locations_y = page_size_y / (font_size * line_size)
        return int(locations_x * locations_y)
