from typing import List

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from qdrant_service.config import QDRANT_CLUSTER_URL, QDRANT_CLUSTER_TOKEN, COLLECTION_NAME

class ImageSearcher:

    def __init__(self):
        self.text_model = SentenceTransformer('sentence-transformers/clip-ViT-B-32-multilingual-v1')
        self.qdrant_client = QdrantClient(
            url=QDRANT_CLUSTER_URL,
            api_key=QDRANT_CLUSTER_TOKEN,
        )

    def search(self, text: str, n_results: str = 10) -> List[dict]:
        text_embedding = self.text_model.encode([text])
        hits = self.qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=text_embedding[0],
            limit=n_results # alias top did not work here
        )
        return hits
