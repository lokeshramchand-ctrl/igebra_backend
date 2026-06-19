from motor.motor_asyncio import AsyncIOMotorClient
import logging
from core.config import settings 
logger = logging.getLogger(__name__)

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

    @classmethod
    async def connect(cls):
        logger.info("Connecting to MongoDB...")
        cls.client = AsyncIOMotorClient(settings.MONGODB_URI)
        cls.db = cls.client[settings.MONGODB_DB_NAME]
        
        # Explicitly declare collections for clarity, though MongoDB creates them lazily
        cls.transactions = cls.db.get_collection("transactions")
        cls.feedback = cls.db.get_collection("feedback")
        cls.categories = cls.db.get_collection("categories")
        cls.merchants = cls.db.get_collection("merchants")
        logger.info("MongoDB connected.")

    @classmethod
    async def disconnect(cls):
        if cls.client:
            logger.info("Closing MongoDB connection...")
            cls.client.close()
            logger.info("MongoDB disconnected.")

db = MongoDB()