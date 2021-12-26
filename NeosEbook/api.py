from typing import List, Optional

from fastapi import APIRouter, Depends, Response

from NeosEbook.database import get_db
from NeosEbook.schema import NeosBookOutList, PageContent
from NeosEbook.service import NeosEbookService

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[NeosBookOutList])
async def list_books(q: Optional[str] = None, db: get_db = Depends()):
    service = NeosEbookService(db)
    await service.add_book_from_path("/Ebooks/Ready Player One by Ernest Cline (z-lib.org).epub")
    books_list = await NeosEbookService(db).get_books(q=q)
    return books_list


@router.get(
    "/{book_uuid}/cover",
    responses={200: {"content": {"image/png": {}}}},
    response_class=Response,
)
async def get_cover(book_uuid: str, db: get_db = Depends()):
    cover = await NeosEbookService(db).get_cover(book_uuid)
    return Response(content=cover, media_type="image/png")


@router.get("/{book_uuid}/page/{page_number}", response_model=PageContent)
async def get_page(book_uuid: str, page_number: int, db: get_db = Depends()):
    page = await NeosEbookService(db).get_page(book_uuid, page_number)
    return page
