"""crate table subjects

Revision ID: bf94b03a5fb0
Revises: a47dc863e8a0
Create Date: 2024-01-16 13:57:09.192708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf94b03a5fb0'
down_revision: Union[str, None] = 'a47dc863e8a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'subjects',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('teacher_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'])
    )


def downgrade():
    op.drop_table('subjects')