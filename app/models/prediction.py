from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id", ondelete="CASCADE"), nullable=False)
    model_id = Column(UUID(as_uuid=True), nullable=True)
    stress_level = Column(String(50), nullable=True)
    stress_probability = Column(Float, nullable=True)
    growth_prediction = Column(Float, nullable=True)
    input_data = Column(JSONB, nullable=True)
    predicted_at = Column(DateTime(timezone=True), server_default=func.now())
