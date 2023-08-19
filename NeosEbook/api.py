from typing import List, Optional

import databases
from fastapi import APIRouter, Depends, Response

from NeosEbook.database import get_db
from NeosEbook.schema import NeosBookOutList, PageContent, BookmarkSerializerModel
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
    book_uuid: str, output_format: str="image", db: databases.Database = Depends(lambda: get_db(config))
):
    cover = await NeosEbookService(db).get_cover(book_uuid, output_format=output_format)
    return Response(content=cover, media_type="image/png")


@router.get("/{book_uuid}/page", response_model=PageContent)
async def get_page(
    book_uuid: str,
    page: Optional[int] = None,
    bookmark: Optional[str] = None,
    db: databases.Database = Depends(lambda: get_db(config)),
):
    page = await NeosEbookService(db).get_page(book_uuid=book_uuid, page_number=page, bookmark_uuid=bookmark)
    return page


@router.post("/{book_uuid}/bookmark")
async def set_bookmark(book_uuid: str, bookmark: BookmarkSerializerModel, db: databases.Database = Depends(lambda: get_db(config))):
    bookmark = await NeosEbookService(db).add_bookmark(book_uuid, bookmark)
    return bookmark

@router.delete("/bookmarks/{bookmark_uuid}")
async def delete_bookmark(bookmark_uuid: str, db: databases.Database = Depends(lambda: get_db(config))):
    return await NeosEbookService(db).remove_bookmark(bookmark_uuid)