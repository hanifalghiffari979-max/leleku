import httpx
from app.core.config import settings
from typing import Optional

async def fetch_latest_from_thingspeak(
    channel_id: str,
    read_key: str,
    results: int = 1
) -> Optional[dict]:
    url = f"{settings.THINGSPEAK_BASE_URL}/channels/{channel_id}/feeds.json"
    params = {"api_key": read_key, "results": results}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            feeds = data.get("feeds", [])
            if not feeds:
                return None
            latest = feeds[-1]

            def safe_float(val):
                try:
                    return float(val) if val else None
                except:
                    return None

            return {
                "ph": safe_float(latest.get("field1")),
                "tds": safe_float(latest.get("field2")),
                "temperature": safe_float(latest.get("field3")),
                "ammonia": safe_float(latest.get("field4")),
                "created_at": latest.get("created_at")
            }
        except Exception as e:
            print(f"ThingSpeak error: {e}")
            return None
