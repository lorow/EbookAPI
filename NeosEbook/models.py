import uuid as uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Book(Base):
    __tablename__ = "neosbooks__books"
    id = Column(Integer, primary_key=True, index=True)
    uuid: Column(UUID(as_uuid=True), default=uuid.uuid4)
    thumbnail: Column(String)
    file_path: Column(String)
    pages: Column(Integer)
    current_page: Column(Integer, default=0)
