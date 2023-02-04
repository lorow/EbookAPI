from fastapi import FastAPI
from NeosEbook.database import get_db
from NeosEbook.settings import config
from NeosEbook.api import router


app = FastAPI()
app.include_router(router)

db = get_db(config)


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
