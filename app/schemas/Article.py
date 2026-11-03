from datetime import datetime

from pydantic import BaseModel


class Article(BaseModel):
    title: str
    url: str
    source: str
    published_at: datetime
    description: str | None = None
    image_url: str | None = None
    summary: str | None = None
