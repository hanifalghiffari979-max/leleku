from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.database import get_db
from app.models.sensor import SensorLog
from app.models.channel import Channel
from app.models.user import User
from app.schemas.sensor import SensorLogCreate, SensorLogResponse, SensorLatest
from app.core.dependencies import get_current_user
from app.services.websocket_manager import manager
from app.services.thingspeak_service import fetch_latest_from_thingspeak
from app.services.scheduler_service import poll_thingspeak
from typing import List
import uuid

router = APIRouter(prefix="/sensors", tags=["Sensors"])

@router.post("/{channel_id}", response_model=SensorLogResponse, status_code=201)
async def add_sensor_data(
    channel_id: uuid.UUID,
    data: SensorLogCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Channel).where(Channel.id == channel_id))
    channel = result.scalar_one_or_none()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel tidak ditemukan")
    if channel.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Akses ditolak")

    log = SensorLog(
        channel_id=channel_id,
        ph=data.ph,
        tds=data.tds,
        temperature=data.temperature,
        ammonia=data.ammonia
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)

    # Broadcast ke WebSocket
    await manager.broadcast_to_channel(str(channel_id), {
        "type": "sensor_update",
        "data": {
            "id": log.id,
            "channel_id": str(log.channel_id),
            "ph": log.ph,
            "tds": log.tds,
            "temperature": log.temperature,
            "ammonia": log.ammonia,
            "recorded_at": log.recorded_at.isoformat()
        }
    })
    return log

@router.get("/{channel_id}/latest", response_model=SensorLatest)
async def get_latest_sensor(
    channel_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(SensorLog)
        .where(SensorLog.channel_id == channel_id)
        .order_by(desc(SensorLog.recorded_at))
        .limit(1)
    )
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=404, detail="Belum ada data sensor")
    return log

@router.get("/{channel_id}/history", response_model=List[SensorLogResponse])
async def get_sensor_history(
    channel_id: uuid.UUID,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(SensorLog)
        .where(SensorLog.channel_id == channel_id)
        .order_by(desc(SensorLog.recorded_at))
        .limit(limit)
    )
    return result.scalars().all()

@router.post("/poll/manual", tags=["Sensors"])
async def manual_poll():
    await poll_thingspeak()
    return {"message": "Polling selesai"}
