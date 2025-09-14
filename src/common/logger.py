import logging
from ecs_logging import StdlibFormatter


logger = logging.getLogger()
logger.setLevel(logging.INFO)

ecs_formatter = StdlibFormatter(exclude_fields=["log.original", "process"])

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(ecs_formatter)

logger.addHandler(stream_handler)