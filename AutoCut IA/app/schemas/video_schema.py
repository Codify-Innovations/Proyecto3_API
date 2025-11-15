from typing import List, Optional
from pydantic import BaseModel

class VideoRequest(BaseModel):
    image_urls: List[str]
    video_urls: List[str]
    style: str
    duration: int
    music_url: Optional[str] = None
