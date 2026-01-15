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
    """
    Adds a new video
    param video: The parameters of the new video that we will be adding
    param db: Session for database
    return: The video that we added
    """
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
    """
    Get a list of videos that we have filtered out.
    param db: Session for database
    param video_filter: Filters to identify suitable videos
    return: A list of videos filtered by parameters
    """
    query = video_filter.filter(select(Video))
    result = await db.execute(query)
    videos = result.scalars().all()
    return videos


@video_router.get("/{video_id}", response_model=VideoRead)
async def get_video_by_id(video_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get the video by the id parameter, if the video is not found, it raise an error
    param video_id: Unique video ID
    param db: Session for database
    return: The video we were looking for by ID
    """
    video = await get_video_or_404(video_id, db)
    return video


@video_router.patch("/{video_id}/status")
async def update_status_video(
    video_id: int, data: VideoStatusUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Putch the status of the video, according to the option set by the user
    param video_id: Unique video ID
    param data_status: Data with the new video status
    param db: Session for database
    return: Modified video with new status
    """
    video = await get_video_or_404(video_id, db)
    video.status = data.status
    db.add(video)
    await db.commit()
    await db.refresh(video)
    return video
