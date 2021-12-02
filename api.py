from .app import app


@app.get("/books/")
def list_all_books():
    return {}


@app.get("/books/{book_uuid}/{page_number}")
def get_page(book_uuid: str, page_nubmer: int):
    return {}
