import asyncio
from temporalio.client import Client
from src.workflows.workflow import NasaWorkflow

async def main():
    client = await Client.connect("localhost:7233")

    result = await client.execute_workflow(
        NasaWorkflow.run,
        id="nasa-workflow-1",
        task_queue="nasa-task-queue",
    )

    print("Resultado do workflow:", result)

if __name__ == "__main__":
    asyncio.run(main())
