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

        self.text_model = SentenceTransformer(\
            'sentence-transformers/clip-ViT-B-32-multilingual-v1')
        self.qdrant_client = QdrantClient(
            url=QDRANT_CLUSTER_URL,
            api_key=QDRANT_CLUSTER_TOKEN,
        )
        self.collection_name = collection_name
        self.vector_size = self.qdrant_client.get_collection(
            self.collection_name
        ).config.params.vectors.size


    # search for a collection of texts and vectors by embedding
    # texts and then performing a vector average over all vectors.
    # The resulting average vector  is then used for similarity search.
    def search(self, q_texts: List[str], q_vectors: List[str],\
                     n_results: str = 10) -> List[dict]:

        if not (q_texts or q_vectors):
            return []

        text_vectors = self.embed_texts(q_texts)
        raw_vectors = np.array(q_vectors)

        if np.any([len(v) != self.vector_size for v in raw_vectors]):
            msg = 'At least one of the provided vectors does not match the\
                   required size {}'.format(self.vector_size)
            raise ValueError(msg)

        vectors = np.concatenate([a for a in [raw_vectors, text_vectors]\
                                    if a.size > 0])

        avg_vector = self.vector_avg(vectors)

        hits = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=avg_vector,
            with_vectors=True,
            limit=n_results
        )
        return hits


    def vector_avg(self, vectors: List[List[float]]) -> List[float]:

        return np.average(np.asarray(vectors), axis = 0)


    def embed_texts(self, texts: List[str]) -> List[List[float]]:

        return np.array(self.text_model.encode(texts))
