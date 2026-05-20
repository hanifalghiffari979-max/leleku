from sqlalchemy import Column, String, Float, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.database import Base

class AIModel(Base):
    __tablename__ = "ai_models"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    version = Column(String(50), nullable=False)
    model_type = Column(String(100), nullable=True)
    accuracy = Column(Float, nullable=True)
    file_url = Column(Text, nullable=True)
    is_active = Column(Boolean, default=False)
    metrics = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
