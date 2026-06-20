from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, utility
import logging

logger = logging.getLogger(__name__)

# Nomic embedding dimension
VECTOR_DIM = 768 

class VectorStoreManager:
    def __init__(self):
        self.behavior_col_name = "behavior_vectors"
        self._ensure_collections()

    def _ensure_collections(self):
        """Creates collections and HNSW indexes if they do not exist."""
        if not utility.has_collection(self.behavior_col_name):
            fields = [
                FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=255),
                FieldSchema(name="merchant_name", dtype=DataType.VARCHAR, max_length=255),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=VECTOR_DIM)
            ]
            schema = CollectionSchema(fields, description="Semantic embeddings of merchant behaviors")
            collection = Collection(name=self.behavior_col_name, schema=schema)
            
            # Create HNSW Index for high-speed approximate nearest neighbor search
            index_params = {
                "metric_type": "COSINE",
                "index_type": "HNSW",
                "params": {"M": 8, "efConstruction": 200}
            }
            collection.create_index(field_name="embedding", index_params=index_params)
            logger.info(f"Created Milvus collection: {self.behavior_col_name}")
        
        self.behavior_collection = Collection(self.behavior_col_name)
        self.behavior_collection.load()

    def insert_behavior_vector(self, pattern_id: str, merchant_name: str, vector: list[float]):
        """Inserts or overwrites a vector in Milvus."""
        data = [
            [pattern_id], 
            [merchant_name], 
            [vector]
        ]
        self.behavior_collection.upsert(data)
        logger.info(f"Inserted vector for entity: {merchant_name}")

vector_store = VectorStoreManager()
