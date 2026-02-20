import asyncio

from src import log
from src.api.backend import BackendClient
from src.source_processing.service import SourceProcessing

tasks = {}


async def main():
    backend_client = BackendClient()
    while True:
        try:
            sources = await backend_client.get_sources()
        except Exception as e:
            log.error(f"Error fetching sources: {e}")
        else:
            source_ids = {source.id for source in sources.sources if not source.disabled}

            for source in sources.sources:
                if not source.disabled and source.id not in tasks:
                    log.info(f"Starting processing for source {source.title} (ID: {source.id})")
                    task = asyncio.create_task(SourceProcessing(source).process())
                    tasks[source.id] = task

            for source_id, task in list(tasks.items()):
                if source_id not in source_ids:
                    log.info(
                        f"Stopping processing for source ID: {source_id} "
                        f"(no longer active or removed)"
                    )
                    task.cancel()
                    del tasks[source_id]

        log.info("Sleeping for 60 seconds before next check...")
        await asyncio.sleep(60)  # Poll every 60 seconds


if __name__ == "__main__":
    asyncio.run(main())
