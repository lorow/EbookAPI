"""create account table

Revision ID: 7077af9276f1
Revises: 
Create Date: 2021-12-05 14:31:28.703755

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.

revision = "7077af9276f1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "neosbooks__books",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.Column("uuid", sa.String()),
        sa.Column("title", sa.String()),
        sa.Column("thumbnail", sa.String(), nullable=True),
        sa.Column("file_path", sa.String()),
        sa.Column("file_format", sa.String()),
        sa.Column("pages", sa.Integer()),
        sa.Column("locations", sa.Integer()),
    )
    op.create_index(
        op.f("ix_neosbooks__books_id"), "neosbooks__books", ["id"], unique=False
    )
    op.create_table(
        "neosbooks__reading_state",
        sa.Column("uuid", sa.String()),
        sa.PrimaryKeyConstraint("uuid"),
        sa.Column("page", sa.Integer(), default=0, nullable=True),
        sa.Column("location", sa.Integer(), default=0, nullable=True),
        sa.Column("progress", sa.Integer(), default=0),
        sa.Column("font_size", sa.Integer(), default=14),
    )
    op.create_index(
        op.f("ix_neosbooks__reading_state_uuid"), "neosbooks__reading_state", ["uuid"], unique=False
    )
    op.create_table(
        "neosbooks__chapter_locations",
        sa.Column("id", sa.String()),
        sa.PrimaryKeyConstraint("id"),
        sa.Column("uuid", sa.String()),
        sa.Column("locations_min", sa.Integer(), default=0),
        sa.Column("locations_max", sa.Integer(), default=0),
    )
    op.create_index(
        op.f("ix_neosbooks__chapter_locations_id"), "neosbooks__chapter_locations", ["id"], unique=False
    )
    op.create_table(
        "ebookapi_bookmarks",
        sa.Column("uuid", sa.String()),
        sa.PrimaryKeyConstraint("uuid"),
        sa.ForeignKey("book_uuid", "neosbooks__books.uuid"),
        sa.ForeignKey("location_id", "neosbooks__chapter_locations.id")
    )
    op.create_index(
        op.f("ix_ebookapi_bookmarks_uuid"), "ebookapi_bookmarks", ["uuid"], unique=False
    )


def downgrade():
    op.drop_index(op.f("ix_neosbooks__books_id"), table_name="neosbooks__books")
    op.drop_index(op.f("ix_neosbooks__reading_state_uuid"), table_name="neosbooks__reading_state")
    op.drop_index(op.f("ix_neosbooks__chapter_locations_id"), table_name="neosbooks__chapter_locations")
    op.drop_index(op.f("ix_ebookapi_bookmarks_uuid"), table_name="ebookapi_bookmarks")
    op.drop_table("neosbooks__books")
    op.drop_table("neosbooks__reading_state")
    op.drop_table("neosbooks__chapter_locations")
    op.drop_table("ebookapi_bookmarks")
