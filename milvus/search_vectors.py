from milvus.insert_vectors import vector_store
from embeddings.generate_embeddings import embedding_generator
import logging

logger = logging.getLogger(__name__)

class VectorSearchEngine:
    async def find_similar_behaviors(self, query_text: str, top_k: int = 5) -> list[dict]:
        """
        Takes an unstructured text query, generates a query vector, 
        and searches Milvus for the closest mathematical behaviors.
        """
        # 1. Generate embedding for the search query using Ollama
        query_vector = await embedding_generator.generate(query_text)

        # 2. Search parameters for HNSW
        search_params = {
            "metric_type": "COSINE",
            "params": {"ef": 64} # Higher 'ef' means more accurate but slightly slower search
        }

        # 3. Execute search
        results = vector_store.behavior_collection.search(
            data=[query_vector],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            output_fields=["merchant_name"]
        )

        # 4. Format outputs for the API router
        formatted_results = []
        for hits in results:
            for hit in hits:
                formatted_results.append({
                    "id": hit.id,
                    "merchant_name": hit.entity.get("merchant_name"),
                    "distance": hit.distance # Cosine distance (1.0 is identical)
                })

        return formatted_results

vector_search = VectorSearchEngine()
