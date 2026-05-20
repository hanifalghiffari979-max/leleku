from sqlalchemy import Column, Float, DateTime, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class SensorLog(Base):
    __tablename__ = "sensor_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id", ondelete="CASCADE"), nullable=False)
    ph = Column(Float, nullable=True)
    tds = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    ammonia = Column(Float, nullable=True)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
