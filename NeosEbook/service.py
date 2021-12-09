from typing import Iterable, Optional

from NeosEbook.models import NeosBook
from NeosEbook.schema import PageContent


class NeosEbookService:
    async def get_books(self, q: Optional[str] = None) -> Iterable[NeosBook]:
        return []

    async def get_page(self, book_uuid, page_number) -> PageContent:
        return PageContent()
