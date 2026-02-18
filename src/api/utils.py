from functools import wraps

import httpx


def retry_on_unauthorized(func):
    """
    Async decorator to retry a function if it raises a 401 Unauthorized error.
    """

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 401:
                await self.login()
                return await func(self, *args, **kwargs)
            raise exc

    return wrapper
