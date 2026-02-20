import asyncio
import time
from datetime import datetime, timezone
from pathlib import Path

from yarl import URL

from src import log
from src.api import TranscriptionClient, get_video_from_archive
from src.api.backend import BackendClient
from src.api.backend.schemas import Source, Transcription, TranscriptionList
from src.source_processing.constants import EXCLUDED_PHRASES
from src.source_processing.utils import delete_file


class SourceProcessing:
    def __init__(self, source: Source) -> None:
        self._chunk_duration = source.chunk_duration
        self._time = self._get_current_time()
        self._transcription_client = TranscriptionClient()
        self._backend_client = BackendClient()
        self._source = source
        self._excluded_phrases_lower = [p.lower() for p in EXCLUDED_PHRASES]

    def _get_current_time(self) -> int:
        """
        Calculates the current time for processing video chunks,
        ensuring that it starts from a point in the past to allow for processing of recent chunks.
        """
        return int(datetime.now(timezone.utc).timestamp()) - (self._chunk_duration * 3 // 2)

    def get_url(self, timestamp: int, duration: int) -> str:
        """
        Constructs the URL for the video chunk based on the source URL,
        timestamp, and duration.
        """
        base_url = URL(self._source.url)

        if base_url.suffix == ".m3u8":
            base_url = base_url.with_name("")

        return str(base_url / f"archive-{timestamp}-{duration}.ts")

    async def _iteration(self):
        """
        Performs a single iteration of processing for the current time chunk
        """
        filepath = Path("data/") / str(self._source.id) / f"{self._time}-{self._chunk_duration}.ts"
        url = self.get_url(
            timestamp=self._time,
            duration=self._chunk_duration,
        )
        try:
            await get_video_from_archive(url, filepath)

            log.debug("Transcribing...")
            transcription_result = await self._transcription_client.transcribe(
                filepath, language=self._source.language
            )

            segments = []
            for segment in transcription_result.segments:
                segment_text_lower = segment.text.lower()
                if all(phrase not in segment_text_lower for phrase in self._excluded_phrases_lower):
                    segment.start += self._time
                    segment.end += self._time
                    segments.append(segment)

            if segments:
                await self._backend_client.send_transcription_result(
                    source_id=self._source.id,
                    transcription=TranscriptionList(
                        transcriptions=[
                            Transcription(
                                start=segment.start,
                                end=segment.end,
                                text=segment.text,
                            )
                            for segment in segments
                        ],
                    ),
                )

        except Exception as e:
            log.error("Error processing chunk", error=e, source_id=self._source.id, time=self._time)
        finally:
            if filepath.exists():
                await delete_file(filepath)

    async def process(self) -> None:
        """
        Main processing loop that continuously processes video chunks
        based on the specified chunk duration.
        """
        while True:
            start_time_counter = time.perf_counter()
            await self._iteration()
            end_time_counter = time.perf_counter()

            duration_execution = end_time_counter - start_time_counter
            log.info("Duration execution: %s", str(duration_execution))

            self._time += self._chunk_duration
            cur_time = self._get_current_time()
            if cur_time - self._time < 0:
                await asyncio.sleep(self._time - cur_time)
