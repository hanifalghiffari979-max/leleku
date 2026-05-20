from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    APP_NAME: str = "Lele Monitoring API"
    DEBUG: bool = True
    THINGSPEAK_BASE_URL: str = "https://api.thingspeak.com"
    THINGSPEAK_CHANNEL_ID: str = ""
    THINGSPEAK_READ_KEY: str = ""
    THINGSPEAK_WRITE_KEY: str = ""

    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
