import httpx

from src.config import settings

from .schemas import SourceList, TranscriptionList
from ... import log


class BackendClient:
    """
    Client for interacting with the backend API.
    """

    def __init__(self):
        self._base_url = settings.BACKEND_BASE_URL
        self._headers: dict[str, str] = {"Authorization": f"Bearer {settings.BACKEND_API_KEY}"}

    async def get_sources(self) -> SourceList:
        """
        Get the list of sources from the backend.
        """
        endpoint = f"{self._base_url}/sources"
        log.debug(
            "Fetching sources from backend",
            endpoint=endpoint
        )
        response = await self._get(endpoint)
        log.debug(
            "Received sources from backend",
            endpoint=endpoint,
            status_code=response.status_code,
            response=response.json()
        )
        return SourceList.model_validate(response.json())

    async def send_transcription_result(
        self, source_id: int, transcription: TranscriptionList
    ) -> None:
        """
        Send the transcription result to the backend.
        """
        endpoint = f"{self._base_url}/transcriptions/{source_id}"
        log.debug(
            f"Sending transcription result",
            source_id=source_id,
            transcription=transcription,
            endpoint=endpoint
        )
        result = await self._post(endpoint, json=transcription.model_dump())
        log.debug(
            f"Received response from backend after sending transcription result",
            source_id=source_id,
            status_code=result.status_code,
            response=result.json()
        )

    async def _post(self, endpoint: str, **kwargs) -> httpx.Response:
        """
        Send an async POST request.
        """
        async with httpx.AsyncClient(headers=self._headers, timeout=60.0) as client:
            response = await client.post(endpoint, **kwargs)
            response.raise_for_status()
            return response

    async def _get(self, endpoint: str, **kwargs) -> httpx.Response:
        """
        Send an async GET request.
        """
        async with httpx.AsyncClient(headers=self._headers, timeout=60.0) as client:
            response = await client.get(endpoint, **kwargs)
            response.raise_for_status()
            return response
