import uuid as uuid

import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from NeosEbook.database import metadata

NeosBook = sqlalchemy.Table(
    "neosbooks__books",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("uuid", UUID(as_uuid=True), default=uuid.uuid4),
    Column("title", String),
    Column("thumbnail", String),
    Column("file_path", String),
    Column("file_format", String),
    Column("pages", Integer),
    Column("locations", Integer),
)


ReadingState = sqlalchemy.Table(
    "neosbooks_reading_state",
    metadata,
    Column("book_uuid", UUID(as_uuid=True)),
    Column("page", Integer, default=0, nullable=True),
    Column("location", Integer, default=0, nullable=True),
    Column("progress", Integer, default=0),
)
