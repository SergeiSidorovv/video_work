from fastapi import FastAPI
from app import api_video

app = FastAPI()
app.include_router(api_video.video_router)
