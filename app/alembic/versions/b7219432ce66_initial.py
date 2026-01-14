"""initial

Revision ID: b7219432ce66
Revises: 
Create Date: 2026-01-14 20:07:51.329850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7219432ce66'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('videos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('video_path', sa.String(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('duration', sa.Interval(), nullable=False),
    sa.Column('camera_number', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_videos'))
    )
    op.create_index(op.f('ix_videos_id'), 'videos', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_videos_id'), table_name='videos')
    op.drop_table('videos')
