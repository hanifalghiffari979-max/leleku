from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class ChannelCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False
    thingspeak_channel_id: Optional[str] = None
    thingspeak_read_key: Optional[str] = None

class ChannelResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    description: Optional[str]
    is_public: bool
    thingspeak_channel_id: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
