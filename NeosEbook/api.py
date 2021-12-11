from typing import Optional, List
from fastapi import APIRouter, Depends

from NeosEbook.database import get_db
from NeosEbook.service import NeosEbookService
from NeosEbook.schema import NeosBookOutList, PageContent

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[NeosBookOutList])
async def list_books(q: Optional[str] = None, db: get_db = Depends()):
    books_list = await NeosEbookService(db).get_books(q=q)
    return books_list


@router.get("/{book_uuid}/{page_number}", response_model=PageContent)
async def get_page(book_uuid: str, page_number: int, db: get_db = Depends()):
    page = await NeosEbookService(db).get_page(book_uuid, page_number)
    return page
