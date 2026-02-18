from pathlib import Path

import aiofiles
import aiohttp

from src import log


async def get_video_from_archive(url: str, filepath: Path) -> None:
    """
    Download video from archive in a safe and controlled way.

    Args:
        url (str): Full URL to the video file
        filepath (Path): Destination path for saving video

    Returns:
        Path: Path to saved file

    Raises:
        RuntimeError: If video file cannot be downloaded
    """

    filepath.parent.mkdir(parents=True, exist_ok=True)

    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            log.debug("download_start", url=url, filepath=str(filepath))
            async with session.get(url, ssl=False) as response:
                response.raise_for_status()

                async with aiofiles.open(filepath, "wb") as f:
                    async for chunk in response.content.iter_chunked(8192):
                        if chunk:
                            await f.write(chunk)

            log.debug("download_success", filepath=str(filepath))

        except Exception as e:
            if filepath.exists():
                filepath.unlink(missing_ok=True)
            log.error("download_error", url=url, filepath=str(filepath), error=str(e))
            raise RuntimeError(f"Error downloading video: {e}") from e
