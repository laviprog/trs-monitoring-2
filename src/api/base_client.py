from abc import ABC, abstractmethod

import httpx

from src.api.utils import retry_on_unauthorized


class BaseClient(ABC):
    """
    Base class for API clients.
    """

    def __init__(self, base_url: str, credentials: dict[str, str]):
        self._base_url = base_url
        self._credentials = credentials
        self._headers: dict[str, str] = {}

    @retry_on_unauthorized
    async def _post(self, endpoint: str, **kwargs) -> httpx.Response:
        """
        Send an async POST request.
        """
        async with httpx.AsyncClient(headers=self._headers, timeout=60.0) as client:
            response = await client.post(endpoint, **kwargs)
            response.raise_for_status()
            return response

    @abstractmethod
    async def login(self) -> None:
        """
        Authenticate and set the Authorization header.
        """
        pass
