from uuid import UUID

from pydantic import BaseModel


class NeosBookBase(BaseModel):
    uuid: UUID
    title: str
    thumbnail: str
    pages: int
    current_page: int
    file_format: str

    class Config:
        orm_mode = True


class NeosBookDB(NeosBookBase):
    id: int
    file_path: str


class NeosBookOutList(BaseModel):
    uuid: UUID
    title: str
    thumbnail: str
    file_format: str


class PageContent(BaseModel):
    uuid: str
    content: str
    page_number: int
