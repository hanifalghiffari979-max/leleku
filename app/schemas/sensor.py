from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List

class SensorLogCreate(BaseModel):
    ph: Optional[float] = None
    tds: Optional[float] = None
    temperature: Optional[float] = None
    ammonia: Optional[float] = None

class SensorLogResponse(BaseModel):
    id: int
    channel_id: UUID
    ph: Optional[float]
    tds: Optional[float]
    temperature: Optional[float]
    ammonia: Optional[float]
    recorded_at: datetime

    model_config = {"from_attributes": True}

class SensorLatest(BaseModel):
    channel_id: UUID
    ph: Optional[float]
    tds: Optional[float]
    temperature: Optional[float]
    ammonia: Optional[float]
    recorded_at: Optional[datetime]
