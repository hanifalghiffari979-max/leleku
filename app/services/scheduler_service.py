from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.channel import Channel
from app.models.sensor import SensorLog
from app.services.thingspeak_service import fetch_latest_from_thingspeak
from datetime import datetime, timezone

scheduler = AsyncIOScheduler()

async def poll_thingspeak():
    print(f"[{datetime.now()}] Polling ThingSpeak...")
    async with AsyncSessionLocal() as db:
        try:
            # Ambil semua channel yang punya thingspeak_channel_id
            result = await db.execute(
                select(Channel).where(
                    Channel.thingspeak_channel_id.isnot(None),
                    Channel.thingspeak_read_key.isnot(None)
                )
            )
            channels = result.scalars().all()

            for channel in channels:
                data = await fetch_latest_from_thingspeak(
                    channel.thingspeak_channel_id,
                    channel.thingspeak_read_key
                )
                if data:
                    log = SensorLog(
                        channel_id=channel.id,
                        ph=data["ph"],
                        tds=data["tds"],
                        temperature=data["temperature"],
                        ammonia=data["ammonia"]
                    )
                    db.add(log)
                    print(f"✅ Data saved for channel: {channel.name}")

            await db.commit()
        except Exception as e:
            print(f"❌ Polling error: {e}")
            await db.rollback()

def start_scheduler():
    scheduler.add_job(
        poll_thingspeak,
        trigger=IntervalTrigger(minutes=5),
        id="thingspeak_polling",
        replace_existing=True
    )
    scheduler.start()
    print("✅ Scheduler started — polling every 5 minutes")

def stop_scheduler():
    scheduler.shutdown()
    print("Scheduler stopped")
