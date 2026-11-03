from pydantic import BaseModel

class Video(BaseModel):
    platform:str
    video_id:str
    url: str
    title : str
    author : str
    stats: VideoStats

class VideoStats(BaseModel):
    likes : int | None = None
    views : int | None = None
    bookmarks : int | None = None
    comments : int | None = None
    shares :int | None = None

class Author(BaseModel):
    author:str
    followers:int
