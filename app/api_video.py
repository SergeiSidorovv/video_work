from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import VideoCreate, VideoRead
from app.models import Video

video_router = APIRouter(prefix="/videos", tags=["Videos"])


@video_router.post("", response_model=VideoRead, status_code=status.HTTP_201_CREATED)
async def create_video(video: VideoCreate, db: AsyncSession = Depends(get_db)):
    db_video = Video(
        video_path=video.video_path,
        start_time=video.start_time,
        duration=video.duration,
        camera_number=video.camera_number,
        location=video.location,
        status="new",
    )
    db.add(db_video)
    await db.commit()
    await db.refresh(db_video)
    return db_video
