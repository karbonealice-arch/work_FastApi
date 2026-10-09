from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field


class Ad(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(description="Unique identifier for the ad")
    title: str
    description: str
    price: float
    author: str
    created_at: datetime
