from datetime import datetime, timedelta
from pydantic import BaseModel, Field, field_validator
from typing import Literal


class VideoCreate(BaseModel):
    video_path: str = Field(..., min_length=1)
    start_time: datetime
    duration: timedelta
    camera_number: int = Field(..., gt=0)
    location: str = Field(..., min_length=1)

    @field_validator("duration")
    @classmethod
    def duration_must_be_positive(cls, values: timedelta):
        if values.total_seconds() <= 0:
            raise ValueError("duration must be positive")
        return values


class VideoRead(BaseModel):
    id: int
    video_path: str
    start_time: datetime
    duration: timedelta
    camera_number: int
    location: str
    status: Literal["new", "transcoded", "recognized"]
    created_at: datetime

    class Config:
        from_attributes = True
