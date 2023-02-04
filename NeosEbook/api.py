from typing import List, Optional

import databases
from fastapi import APIRouter, Depends, Response

from NeosEbook.database import get_db
from NeosEbook.schema import NeosBookOutList, PageContent
from NeosEbook.service import NeosEbookService
from NeosEbook.settings import config

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[NeosBookOutList])
async def list_books(
    q: Optional[str] = None, db: databases.Database = Depends(lambda: get_db(config))
):
    books_list = await NeosEbookService(db).get_books(q=q)
    return books_list


@router.get(
    "/{book_uuid}/cover",
    responses={200: {"content": {"image/png": {}}}},
    response_class=Response,
)
async def get_cover(
    book_uuid: str, db: databases.Database = Depends(lambda: get_db(config))
):
    cover = await NeosEbookService(db).get_cover(book_uuid)
    return Response(content=cover, media_type="image/png")


@router.get("/{book_uuid}/page", response_model=PageContent)
async def get_page(
    book_uuid: str,
    page: Optional[int] = None,
    db: databases.Database = Depends(lambda: get_db(config)),
):
    page = await NeosEbookService(db).get_page(book_uuid, page)
    return page
