import asyncio
from temporalio.client import Client

from src.workflows.workflow import NasaWorkflow
from src.common.config import settings


async def main():
    client = await Client.connect(settings.temporal_host)

    event = {
        "inputs": {"start_time": "2025-09-01", "end_time": "2025-09-02"},
    }

    result = await client.execute_workflow(
        NasaWorkflow.run,
        event,
        id="study-workflow-1",
        task_queue=settings.temporal_task_queue,
    )

    print("Resultado do workflow:", result)


if __name__ == "__main__":
    asyncio.run(main())
