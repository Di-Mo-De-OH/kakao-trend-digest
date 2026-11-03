from pydantic import BaseModel, field_validator

from app.core.utils import normalize_tag


class Hashtag(BaseModel):
    name: str
    rank: int
    rank_change: int | None = None
    is_new: bool = False
    posts: int | None = None
    views: int | None = None
    category: str | None = None
    url: str | None = None

    @field_validator("name")
    @classmethod
    def normalize_name(cls, v: str) -> str:
        return normalize_tag(v)
