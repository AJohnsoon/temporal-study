import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from src.workflows.workflow import NasaWorkflow
from src.activities.activities import fetch_nasa_apod, fetch_nasa_neows

import asyncio
from aiohttp import web

from temporalio.worker import Worker
from temporalio.client import Client
from temporalio.runtime import (
    Runtime,
    TelemetryConfig,
    PrometheusConfig,
    LoggingConfig,
    LogForwardingConfig,
)

from src.common.config import settings
from src.common.logger import logger


async def health_check(request):
    client: Client = request.app["temporal_client"]
    if not client:
        return web.Response(text="Temporal client not initialized", status=500)

    try:
        client.list_workflows(rpc_timeout=5.0)
    except Exception as e:
        return web.Response(text=f"Error connecting to Temporal: {str(e)}", status=500)

    return web.json_response(data={"status": "ok"}, status=200)

async def setup_http_server(temporal_client: Client):
    app = web.Application()
    app["temporal_client"] = temporal_client

    app.router.add_get("/health", health_check)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=settings.http_port)
    await site.start()

async def start_temporal_client() -> Client:
    temporal_runtime = Runtime(
        telemetry=TelemetryConfig(
            metrics=PrometheusConfig(
                bind_address="0.0.0.0:" + str(settings.metrics_port)
            ),
            logging=LoggingConfig(
                filter="temporal_sdk_core=info",
                forwarding=LogForwardingConfig(logger=logger),
            ),
        ),
    )

    return await Client.connect(
        target_host=settings.temporal_host,
        namespace=settings.temporal_namespace,
        runtime=temporal_runtime,
    )

async def run_worker():

    client = await start_temporal_client()
    logger.info(
        settings.metrics_port,
    )

    await setup_http_server(client)
    logger.info("Started HTTP server. Listening on port '%d'", settings.http_port)

    worker = Worker(
            client,
            task_queue=settings.temporal_task_queue,
            workflows=[NasaWorkflow],
            activities=[fetch_nasa_apod, fetch_nasa_neows],
        )

    await worker.run()

def run():
    asyncio.run(run_worker())

if __name__ == "__main__":
    asyncio.run(run())

