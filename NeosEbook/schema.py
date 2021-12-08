from pydantic import BaseModel


class NeosBookBase(BaseModel):
    uuid: str
    title: str
    thumbnail: str
    pages: int
    current_page: int = 0

    class Config:
        orm_mode = True


class NeosBookDB(NeosBookBase):
    id: int
    file_path: str


class NeosBookOutDetail(NeosBookBase):
    pass


class NeosBookOutList:
    uuid: str
    title: str
    thumbnail: str
