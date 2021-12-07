"""create account table

Revision ID: 7077af9276f1
Revises: 
Create Date: 2021-12-05 14:31:28.703755

"""
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy.dialects.postgresql import UUID

revision = "7077af9276f1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "neosbooks__books",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.Column("uuid", sa.String(), default=uuid.uuid4),
        sa.Column("thumbnail", sa.String(), nullable=True),
        sa.Column("file_path", sa.String()),
        sa.Column("pages", sa.Integer()),
        sa.Column("current_page", sa.Integer(), default=0)
    )
    op.create_index(
        op.f("ix_neosbooks__books_id"), "neosbooks__books", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_neosbooks__books_uuid"), "neosbooks__books", ["uuid"], unique=False
    )


def downgrade():
    op.drop_index(op.f("ix_neosbooks__books_id"), table_name="neosbooks__books")
    op.drop_index(op.f("ix_neosbooks__books_uuid"), table_name="neosbooks__books")
    op.drop_table("neosbooks__books")
