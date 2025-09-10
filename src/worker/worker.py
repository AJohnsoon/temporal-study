import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from src.workflows.workflow import NasaWorkflow
from src.activities.activities import fetch_nasa_apod

async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="nasa-task-queue",
        workflows=[NasaWorkflow],
        activities=[fetch_nasa_apod],
    )

    print("Worker iniciado.\nEsperando workflows...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
