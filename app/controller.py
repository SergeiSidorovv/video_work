from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException
from sqlalchemy import select

from app.models import Video


async def get_video_or_404(video_id: int, db: AsyncSession) -> Video:
    query = select(Video).where(Video.id == video_id)
    result = await db.execute(query)
    video = result.scalar_one_or_none()
    if video is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Video {video_id} not found"
        )
    return video
