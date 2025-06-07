import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "erp")
    MONGO_DB_COL: str = os.getenv("MONGO_DB_COL", "documents")
    AUTH0_DOMAIN: str = os.getenv("AUTH0_DOMAIN", "")
    AUTH0_API_AUDIENCE: str = os.getenv("AUTH0_API_AUDIENCE", "")
    LOCAL_STORAGE_PATH: str = os.getenv("LOCAL_STORAGE_PATH", "./storage")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

@lru_cache()
def get_settings() -> Settings:
    return Settings()
