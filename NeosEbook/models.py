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
    "neosbooks__reading_state",
    metadata,
    Column("uuid", UUID(as_uuid=True)),
    Column("page", Integer, default=0, nullable=True),
    Column("location", Integer, default=0, nullable=True),
    Column("progress", Integer, default=0),
    Column("font_size", Integer, default=14),
)


ChapterLocations = sqlalchemy.Table(
    "neosbooks__chapter_locations",
    metadata,
    Column("id", String),
    Column("uuid", UUID(as_uuid=True)),
    Column("locations_min", Integer, default=0),
    Column("locations_max", Integer, default=0),
)
