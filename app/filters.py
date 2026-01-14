from typing import Optional, List
from datetime import datetime
from pydantic import Field, ConfigDict

from fastapi_filter.contrib.sqlalchemy import Filter
from app.models import Video


class VideoFilter(Filter):

    status: Optional[List[str]] = None
    camera_number: Optional[List[int]] = None
    location: Optional[List[str]] = None
    start_time__gte: Optional[datetime] = Field(None, alias="start_time_from")
    start_time__lte: Optional[datetime] = Field(None, alias="start_time_to")

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )

    class Constants(Filter.Constants):
        model = Video
