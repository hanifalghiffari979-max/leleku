from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.channel import Channel
from app.models.user import User
from app.schemas.channel import ChannelCreate, ChannelResponse
from app.core.dependencies import get_current_user
from typing import List
import uuid

router = APIRouter(prefix="/channels", tags=["Channels"])

@router.post("/", response_model=ChannelResponse, status_code=201)
async def create_channel(
    data: ChannelCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    channel = Channel(
        user_id=current_user.id,
        name=data.name,
        description=data.description,
        is_public=data.is_public,
        thingspeak_channel_id=data.thingspeak_channel_id,
        thingspeak_read_key=data.thingspeak_read_key
    )
    db.add(channel)
    await db.commit()
    await db.refresh(channel)
    return channel

@router.get("/", response_model=List[ChannelResponse])
async def get_my_channels(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Channel).where(Channel.user_id == current_user.id)
    )
    return result.scalars().all()

@router.get("/public", response_model=List[ChannelResponse])
async def get_public_channels(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Channel).where(Channel.is_public == True)
    )
    return result.scalars().all()

@router.get("/{channel_id}", response_model=ChannelResponse)
async def get_channel(
    channel_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Channel).where(Channel.id == channel_id))
    channel = result.scalar_one_or_none()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel tidak ditemukan")
    if not channel.is_public and channel.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Akses ditolak")
    return channel
