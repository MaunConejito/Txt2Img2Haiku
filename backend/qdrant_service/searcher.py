from typing import List
import requests
from io import BytesIO
from PIL import Image
import numpy as np

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from qdrant_service.config import QDRANT_CLUSTER_URL, QDRANT_CLUSTER_TOKEN

class Searcher:

    def __init__(self, collection_name):
        self.text_model = SentenceTransformer('sentence-transformers/clip-ViT-B-32-multilingual-v1')
        self.qdrant_client = QdrantClient(
            url=QDRANT_CLUSTER_URL,
            api_key=QDRANT_CLUSTER_TOKEN,
        )
        self.collection_name = collection_name

    def search(self, texts: List[str], vectors: List[str],\
                     n_results: str = 10) -> List[dict]:

        text_embeddings = self.embed_texts(texts)
        vectors = np.array(vectors)
        vectors = np.concatenate([a for a in [vectors,\
                    text_embeddings] if a.size > 0])

        avg_vector = self.vector_avg(vectors)

        hits = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=avg_vector,
            with_vectors=True,
            limit=n_results
        )
        return hits


    def vector_avg(self, vectors: List[List[float]]) -> List[float]:
        vectors = np.asarray(vectors)
        if vectors.dtype=='O':
            print('Could not average vectors. Return first.')
            return vectors[0]
        return np.average(vectors, axis = 0)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        return self.text_model.encode(texts)
