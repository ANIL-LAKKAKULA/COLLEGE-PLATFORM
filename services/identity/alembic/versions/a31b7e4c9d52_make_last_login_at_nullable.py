"""Allow users to be created before their first login.

Revision ID: a31b7e4c9d52
Revises: e14ec9d85fe3
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a31b7e4c9d52"
down_revision: Union[str, Sequence[str], None] = "e14ec9d85fe3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "last_login_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=True,
    )


def downgrade() -> None:
    # Existing rows must be given a value before restoring NOT NULL.
    op.execute(
        sa.text("UPDATE users SET last_login_at = COALESCE(last_login_at, updated_at)")
    )
    op.alter_column(
        "users",
        "last_login_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
    )
