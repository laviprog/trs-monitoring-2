from pydantic import BaseModel, Field


class Transcription(BaseModel):
    start: float
    end: float
    text: str


class TranscriptionList(BaseModel):
    transcriptions: list[Transcription]


class Source(BaseModel):
    id: int
    title: str
    url: str
    language: str
    disabled: bool
    chunk_duration: int = Field(alias="chunkDuration")

    model_config = {"populate_by_name": True}


class SourceList(BaseModel):
    sources: list[Source]
