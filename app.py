from fastapi import FastAPI
from .utils import get_db
from . import api as neos_books_api

db = get_db()
app = FastAPI()
app.include_router(neos_books_api.router)


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
