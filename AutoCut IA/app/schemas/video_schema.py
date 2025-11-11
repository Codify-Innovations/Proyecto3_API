from pydantic import BaseModel
from typing import List

class VideoRequest(BaseModel):
    image_urls: List[str]
    duration: int = 3
    style: str = "cinematic"
