import abc
import os
import uuid
from typing import List, Optional, Type

import ebooklib
from ebooklib import epub

from NeosEbook import exceptions
from NeosEbook import constants
from NeosEbook.schema import NeosBookDB


class BaseBookStrategy(abc.ABC):
    def __init__(self, book: Optional[NeosBookDB] = None, ebook_file_path: str = None):
        self.book = book

    async def get_menu(self):
        raise NotImplementedError

    async def get_page(self, number) -> dict:
        raise NotImplementedError

    async def get_cover(self) -> bytearray:
        raise NotImplementedError

    async def get_book_data(self, book_path: str) -> dict:
        raise NotImplementedError

    async def get_locations_data(self, book_uuid) -> dict:
        raise NotImplementedError


class EPUBBookStrategy(BaseBookStrategy):

    def __init__(self, book=None, ebook_file_path=None):
        super(EPUBBookStrategy, self).__init__(book)
        self.epub_book: Optional[epub.EpubBook] = None
        if ebook_file_path:
            self.epub_book = self._get_epub_from_path(ebook_file_path)

    async def get_page(self, number: int):
        pass

    async def get_menu(self):
        pass

    async def get_cover(self) -> bytearray:
        if not self.epub_book:
            return None

        cover_chapter = self.epub_book.get_item_with_id(self.book.thumbnail)
        return cover_chapter.content

    async def get_book_data(self, book_path: str):
        if not self.epub_book:
            return {}

        book_uuid = uuid.uuid4()
        pages = len(self.epub_book.pages)
        book_data = {
            "uuid": book_uuid,
            "title": self.epub_book.title,
            "thumbnail": await self._get_cover_chapter_id(self.epub_book),
            "pages": pages,
            "file_path": book_path,
            "locations": 0,
            "file_format": "epub",
        }

        return book_data

    async def get_locations_data(self, book_uuid: str):
        locations_stats = {"total": 0, "per_chapter": []}

        if not self.epub_book:
            return locations_stats

        chapters = [item for item in self.epub_book.get_items_of_type(ebooklib.ITEM_DOCUMENT) if item.is_chapter()]

        total_words_count = sum([len(item.content) for item in chapters]) // constants.LOCATION
        if total_words_count:
            locations_stats["total"] = total_words_count // constants.LOCATION
            locations_stats["per_chapter"] = await self._get_chapter_locations_ranges(
                book_uuid=book_uuid,
                index=0,
                chapters=chapters,
                data=[],
                previous_chapter=None,
            )

        return locations_stats

    @staticmethod
    async def _get_cover_chapter_id(book: epub.EpubBook):
        """
        Save the ID of the chapter which holds the cover image.
        This way we can save space and send it right away on request
        """
        for item in book.items:
            if (isinstance(item, epub.EpubImage) and "cover" in item.file_name) or isinstance(item, epub.EpubCover):
                return item.id

    @staticmethod
    def _get_epub_from_path(book_path) -> epub.EpubBook:
        base_file_dir = os.path.dirname(os.path.dirname(__file__))
        ebook_path = f"{base_file_dir}{book_path}"
        epub_book = epub.read_epub(ebook_path)
        return epub_book

    async def _get_chapter_locations_ranges(
        self,
        book_uuid,
        index,
        chapters,
        data,
        previous_chapter=None,
    ) -> List[dict]:
        current_chapter = chapters[index]
        chapter_id = current_chapter.id
        locations_in_chapter = len(current_chapter.content) // constants.LOCATION

        locations_min = previous_chapter.get("locations_max") + 1 if previous_chapter else 0
        locations_max = (
            previous_chapter.get("locations_max") + locations_in_chapter if previous_chapter else locations_in_chapter
        )
        data.append(
            {
                "id": chapter_id,
                "uuid": book_uuid,
                "locations_min": locations_min,
                "locations_max": locations_max,
            }
        )

        if index == len(chapters) - 1:
            return data

        return await self._get_chapter_locations_ranges(
            book_uuid=book_uuid,
            index=index + 1,
            chapters=chapters,
            data=data,
            previous_chapter=data[index],
        )


async def get_ebook_processing_strategy(file_extension: str) -> Type[BaseBookStrategy]:
    strategy_map = {"epub": EPUBBookStrategy}
    strategy = strategy_map.get(file_extension, None)

    if not strategy:
        raise exceptions.StrategyNotImplementedException()

    return strategy
