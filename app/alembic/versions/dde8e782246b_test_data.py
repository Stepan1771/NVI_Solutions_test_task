"""test_data

Revision ID: dde8e782246b
Revises: b7219432ce66
Create Date: 2026-01-14 20:19:42.587176

"""
from datetime import datetime, timedelta
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dde8e782246b'
down_revision: Union[str, Sequence[str], None] = 'b7219432ce66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    op.bulk_insert(
        sa.table(
            "videos",
            sa.column("video_path", sa.String),
            sa.column("start_time", sa.DateTime),
            sa.column("duration", sa.Interval),
            sa.column("camera_number", sa.Integer),
            sa.column("location", sa.String),
            sa.column("status", sa.String),
            sa.column("created_at", sa.DateTime),
        ),
        [
            {
                "video_path": "/videos/video1.mp4",
                "start_time": datetime(2026, 1, 10, 8, 0),
                "duration": timedelta(minutes=5),
                "camera_number": 1,
                "location": "Entrance",
                "status": "new",
                "created_at": datetime.now(),
            },
            {
                "video_path": "/videos/video2.mp4",
                "start_time": datetime(2026, 1, 10, 9, 0),
                "duration": timedelta(minutes=10),
                "camera_number": 2,
                "location": "Lobby",
                "status": "new",
                "created_at": datetime.now(),
            },
            {
                "video_path": "/videos/video3.mp4",
                "start_time": datetime(2026, 1, 10, 10, 0),
                "duration": timedelta(minutes=15),
                "camera_number": 1,
                "location": "Hall",
                "status": "new",
                "created_at": datetime.now(),
            },
            {
                "video_path": "/videos/video4.mp4",
                "start_time": datetime(2026, 1, 10, 11, 0),
                "duration": timedelta(minutes=7),
                "camera_number": 3,
                "location": "Corridor",
                "status": "new",
                "created_at": datetime.now(),
            },
            {
                "video_path": "/videos/video5.mp4",
                "start_time": datetime(2026, 1, 10, 12, 0),
                "duration": timedelta(minutes=12),
                "camera_number": 2,
                "location": "Parking",
                "status": "new",
                "created_at": datetime.now(),
            },
        ]
    )


def downgrade() -> None:
    conn = op.get_bind()

    conn.execute("DELETE FROM videos")


