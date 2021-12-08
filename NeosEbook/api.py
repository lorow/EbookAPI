from fastapi import APIRouter


router = APIRouter(prefix="/books", tags=["books"])


@router.get("/")
async def list_all_books():
    return {}


@router.get("/{book_uuid}/{page_number}")
async def get_page(book_uuid: str, page_number: int):
    return {}


@router.get("/search")
async def search_for_book(title: str):
    return {}
