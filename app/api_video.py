from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi_filter import FilterDepends

from app.controller import get_video_or_404
from app.database import get_db
from app.schemas import VideoCreate, VideoRead, VideoStatusUpdate
from app.models import Video
from app.filters import VideoFilter

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


@video_router.get("")
async def get_videos(
    db: AsyncSession = Depends(get_db),
    video_filter: VideoFilter = FilterDepends(VideoFilter),
):
    query = video_filter.filter(select(Video))
    result = await db.execute(query)
    videos = result.scalars().all()
    return videos


@video_router.get("/{video_id}", response_model=VideoRead)
async def get_video_by_id(video_id: int, db: AsyncSession = Depends(get_db)):
    video = await get_video_or_404(video_id, db)
    return video


@video_router.patch("/{video_id}/status")
async def update_status_video(
    video_id: int, data: VideoStatusUpdate, db: AsyncSession = Depends(get_db)
):
    video = await get_video_or_404(video_id, db)
    video.status = data.status
    db.add(video)
    await db.commit()
    await db.refresh(video)
    return video
