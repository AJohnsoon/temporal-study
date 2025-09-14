from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class TemporalWorkerSettings(BaseSettings):

    # Temporal config
    temporal_host: str = Field(alias="TEMPORAL_HOST")
    temporal_namespace: str = Field(alias="TEMPORAL_NAMESPACE")
    temporal_task_queue: str = Field(alias="TEMPORAL_TASK_QUEUE")

    # HTTP server config
    http_port: int = Field(default=8080, alias="HTTP_PORT")
    metrics_port: int = Field(default=8090, alias="METRICS_PORT")

    # External service config
    service_host: str = Field(alias="SERVICE_HOST")
    service_apikey: str = Field(alias="SERVICE_APIKEY")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = TemporalWorkerSettings()