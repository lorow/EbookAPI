import uuid as uuid

import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer

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
    Column("current_page", Integer, default=0),
)
