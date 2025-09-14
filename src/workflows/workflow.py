from datetime import timedelta
from temporalio import workflow

from src.common.payload import PayloadRequest

@workflow.defn
class NasaWorkflow:
    @workflow.run
    async def run(self, request: PayloadRequest) -> dict:
        
        print("Payload >>>>>>>", request)
        result = await workflow.execute_activity(
            "fetch_nasa_neows",
            request,
            task_queue="study-task-queue",
            schedule_to_close_timeout=timedelta(seconds=10),
        )
        print(result)
        return result
