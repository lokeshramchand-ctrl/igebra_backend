import logging
from pymilvus import MilvusClient
from core.config import settings

logger = logging.getLogger(__name__)

class VectorDB:
    client: MilvusClient | None = None

    @classmethod
    def connect(cls):
        logger.info("Connecting to Milvus...")
        try:
            cls.client = MilvusClient(uri=settings.MILVUS_URI, secure=True)
            logger.info("Milvus connected successfully.")
        except Exception as e:
            logger.error(f"Failed to connect to Milvus: {e}")
            cls.client = None

    @classmethod
    def disconnect(cls):
        if cls.client:
            logger.info("Disconnecting from Milvus...")
            cls.client.close()
            cls.client = None

vector_db = VectorDB()
