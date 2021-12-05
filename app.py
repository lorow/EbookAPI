from fastapi import FastAPI
from utils import get_db


db = get_db()
app = FastAPI()


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
