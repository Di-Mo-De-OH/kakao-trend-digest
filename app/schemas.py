from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class Author(BaseModel):
    username: str
    followers: int


class VideoStats(BaseModel):
    views: int
    likes: int | None = None
    saves: int | None = None
    comments: int | None = None
    shares: int | None = None


class Video(BaseModel):
    platform: Literal["tiktok", "youtube", "instagram"]
    video_id: str
    url: str
    title: str
    author: Author
    stats: VideoStats
    published_at: datetime
    thumbnail_url: str | None = None
    hashtags: list[str] = []
