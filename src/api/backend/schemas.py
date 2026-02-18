from pydantic import BaseModel


class Segment(BaseModel):
    start: float
    end: float
    text: str


class Transcription(BaseModel):
    source_id: int
    segments: list[Segment]


class Source(BaseModel):
    id: int
    title: str
    archive_url: str
    chunk_duration: int


class SourceList(BaseModel):
    sources: list[Source]
