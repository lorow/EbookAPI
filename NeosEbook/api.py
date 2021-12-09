from typing import Optional, List

from fastapi import APIRouter

from NeosEbook.schema import NeosBookOutList, PageContent
from NeosEbook.service import NeosEbookService

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[NeosBookOutList])
async def list_books(q: Optional[str] = None):
    service = NeosEbookService()
    books_list = await service.get_books(q=q)
    return books_list


@router.get("/{book_uuid}/{page_number}", response_model=PageContent)
async def get_page(book_uuid: str, page_number: int):
    service = NeosEbookService()
    page = await service.get_page(book_uuid, page_number)
    return page
