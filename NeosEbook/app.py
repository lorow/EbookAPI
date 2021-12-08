from dotenv import load_dotenv
from fastapi import FastAPI
from NeosEbook.utils import get_db
from NeosEbook.api import router

load_dotenv()

db = await get_db()
app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
