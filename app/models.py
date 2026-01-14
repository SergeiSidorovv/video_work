from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Interval,
    CheckConstraint,
    func,
)
from app.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    video_path = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    duration = Column(Interval, nullable=False)
    camera_number = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("camera_number > 0", name="check_camera_number_positive"),
        CheckConstraint("duration > interval '0'", name="check_duration_positive"),
        CheckConstraint(
            "status IN ('new', 'transcoded', 'recognized')", name="check_status_valid"
        ),
    )
