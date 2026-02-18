from pydantic import BaseModel


class Segment(BaseModel):
    number: int
    start: float
    end: float
    text: str


class WordSegment(BaseModel):
    word: str
    start: float
    end: float
    score: float


class TranscriptionResult(BaseModel):
    segments: list[Segment]
    words: list[WordSegment] | None = None
