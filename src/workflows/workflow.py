from datetime import timedelta
from temporalio import workflow

@workflow.defn
class NasaWorkflow:
    @workflow.run
    async def run(self) -> dict:
        result = await workflow.execute_activity(
            "fetch_nasa_apod",
            schedule_to_close_timeout=timedelta(seconds=10),
        )
        # print(result)
        return result
