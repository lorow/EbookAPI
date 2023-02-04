import abc
import os
import uuid
from typing import List, Optional, Type

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub

from NeosEbook import constants, exceptions
from NeosEbook.repository import ChapterLocationsRepository
from NeosEbook.schema import NeosBookDB, ReadingState


class BaseBookStrategy(abc.ABC):
    def __init__(self, book: Optional[NeosBookDB] = None, ebook_file_path: str = None):
        self.book = book

    async def get_menu(self):
        raise NotImplementedError

    async def get_page(self, number, chapters_repository, reading_state) -> dict:
        raise NotImplementedError

    async def get_cover(self) -> bytearray:
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


class EPUBBookStrategy(BaseBookStrategy):
    def __init__(self, book=None, ebook_file_path=None):
        super(EPUBBookStrategy, self).__init__(book)
        self.epub_book: Optional[epub.EpubBook] = None
        if ebook_file_path:
            self.epub_book = self._get_epub_from_path(ebook_file_path)

    async def get_page(
        self,
        number: int,
        chapters_repository: ChapterLocationsRepository,
        reading_state: ReadingState,
    ) -> Optional[dict]:
        page_data = {
            "uuid": self.book.uuid,
        }

        if not self.epub_book:
            return None

        if self.book.pages:
            page = self.epub_book.pages[number]
            page_data.update(
                {
                    "content": BeautifulSoup(
                        page.get_content(), "html.parser"
                    ).get_text(),
                    "next_page": min(self.book.pages, number + 1),
                    "previous_page": max(number - 1, 0),
                }
            )

        if self.book.locations:
            locations_by_font = (
                await self._get_amount_of_locations_per_page_by_font_size(
                    reading_state.font_size
                )
            )
            chapter = await chapters_repository.get_chapter_by_location(
                self.book.uuid, number
            )
            page = self.epub_book.get_item_with_id(chapter.id)

            chapter_content = BeautifulSoup(
                page.get_content(), "html.parser"
            ).get_text()

            page_data.update(
                {
                    "content": chapter_content[
                        (number - chapter.locations_min)
                        * constants.LOCATION : locations_by_font
                        * constants.LOCATION
                    ],
                    "next_page": number + locations_by_font,
                    "previous_page": max(number - locations_by_font, 0),
                }
            )

        return page_data

    async def get_menu(self):
        pass

    async def get_cover(self) -> Optional[bytearray]:
        if not self.epub_book:
            return None

        cover_chapter = self.epub_book.get_item_with_id(self.book.thumbnail)
        return cover_chapter.content

    async def get_book_data(self, book_path: str):
        if not self.epub_book:
            return {}

        book_uuid = uuid.uuid4()
        pages = len(self.epub_book.pages)
        return {
            "uuid": book_uuid,
            "title": self.epub_book.title,
            "thumbnail": await self._get_cover_chapter_id(self.epub_book),
            "pages": pages,
            "file_path": book_path,
            "locations": 0,
            "file_format": "epub",
        }

    async def get_locations_data(self, book_uuid: str):
        locations_stats = {"total": 0, "per_chapter": []}

        if not self.epub_book:
            return locations_stats

        chapters = [
            item
            for item in self.epub_book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
            if item.is_chapter()
        ]
        if total_words_count := sum(len(item.get_body_content()) for item in chapters):
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
            if (
                isinstance(item, epub.EpubImage) and "cover" in item.file_name
            ) or isinstance(item, epub.EpubCover):
                return item.id

    @staticmethod
    def _get_epub_from_path(book_path) -> epub.EpubBook:
        base_file_dir = os.path.dirname(os.path.dirname(__file__))
        ebook_path = f"{base_file_dir}{book_path}"
        return epub.read_epub(ebook_path)

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
        locations_in_chapter = (
            len(current_chapter.get_body_content()) // constants.LOCATION
        )
        locations_min = (
            previous_chapter.get("locations_max") + 1 if previous_chapter else 0
        )
        locations_max = (
            previous_chapter.get("locations_max") + locations_in_chapter
            if previous_chapter
            else locations_in_chapter
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
    strategy = strategy_map.get(file_extension)

    if not strategy:
        raise exceptions.StrategyNotImplementedException()

    return strategy
