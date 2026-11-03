from datetime import datetime

from pydantic import BaseModel


class Article(BaseModel):
    title: str
    url: str
    source: str
    published_at: datetime
    description: str | None = None
    image_url: str | None = None
    # AI 단계에서 채워지는 값
    summary: str | None = None
