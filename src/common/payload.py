from typing import Dict, Any
from pydantic import BaseModel, Field


class PayloadRequest(BaseModel):
    inputs: Dict[str, Any] = Field(default_factory=dict)
