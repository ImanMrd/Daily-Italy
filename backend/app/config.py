import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "Daily-Italy — Italian Language Mastery"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dailyitaly-secret-key-super-secure-production-ready")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days token for seamless study
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./backend/data/italian_vocab.db")
    CORS_ORIGINS: list[str] = ["*"]

settings = Settings()
