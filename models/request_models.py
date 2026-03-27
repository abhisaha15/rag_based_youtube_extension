from pydantic import BaseModel

class VideoRequest(BaseModel):
    youtube_url: str
    question: str = "Summarize the video"