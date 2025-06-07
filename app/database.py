from motor.motor_asyncio import AsyncIOMotorClient
from .config import get_settings

settings = get_settings()
client = AsyncIOMotorClient(settings.MONGODB_URI)
db = client[settings.MONGO_DB_NAME]
collection = db[settings.MONGO_DB_COL]
