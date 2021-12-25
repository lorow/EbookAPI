from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class NeosBookBase(BaseModel):
    uuid: UUID
    title: str
    thumbnail: str
    pages: int
    locations: int
    file_format: str

    class Config:
        orm_mode = True


class NeosBookDB(NeosBookBase):
    id: int
    file_path: str


class NeosBookOutList(BaseModel):
    uuid: UUID
    title: str
    file_format: str


class PageContent(BaseModel):
    uuid: str
    content: str
    page_number: int


class ChapterLocationsDB(BaseModel):
    """
    Model used for efficiently searching from which chapter to read data
     based on locations
    """

    id: str
    uuid: str
    locations_min: int
    locations_max: int

    class Config:
        orm_mode = True


class ReadingState(BaseModel):
    uuid: str
    page: Optional[int]
    location: Optional[int]
    progress: int

    class Config:
        orm_mode = True
