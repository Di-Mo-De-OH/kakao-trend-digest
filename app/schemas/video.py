from datetime import datetime
from typing import Literal

from pydantic import BaseModel, field_validator

from app.core.utils import normalize_tag


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

    @field_validator("hashtags")
    @classmethod
    def normalize_hashtags(cls, v: list[str]) -> list[str]:
        return [normalize_tag(t) for t in v]
