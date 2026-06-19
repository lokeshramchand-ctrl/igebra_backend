from pymilvus import connections, utility
import logging
from core.config import settings
logger = logging.getLogger(__name__)

class VectorDB:
    @classmethod
    def connect(cls):
        logger.info("Connecting to Milvus...")
        try:
            connections.connect(
                alias="default",
                host=settings.MILVUS_HOST,
                port=settings.MILVUS_PORT,
                secure=True
            )
            logger.info("Milvus connected successfully.")
        except Exception as e:
            logger.error(f"Failed to connect to Milvus: {e}")
    @classmethod
    def disconnect(cls):
        logger.info("Disconnecting from Milvus...")
        connections.disconnect("default")

vector_db = VectorDB()