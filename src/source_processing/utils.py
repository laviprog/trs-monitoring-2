import asyncio
import os
from datetime import datetime
from pathlib import Path

from src import log


async def delete_file(path: str | Path) -> None:
    """
    Asynchronously deletes a file at the specified path.

    :param path: Path (str or Path) to the file to be deleted.
    """
    try:
        await asyncio.to_thread(os.remove, str(path))
    except FileNotFoundError as e:
        log.error("file_not_found", path=str(path), error=str(e))


def normalize_time(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")
