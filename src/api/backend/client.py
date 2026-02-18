import httpx

from src.config import settings

from .schemas import SourceList, Transcription


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
        ...

    async def send_transcription_result(self, transcription: Transcription) -> None:
        """
        Send the transcription result to the backend.
        """
        ...

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
