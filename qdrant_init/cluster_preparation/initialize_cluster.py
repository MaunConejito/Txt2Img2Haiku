import os
import numpy as np

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams

from cluster_preparation.config import QDRANT_CLUSTER_URL,\
                QDRANT_CLUSTER_TOKEN, IMG_COLLECTION_NAME,\
                HAIKU_COLLECTION_NAME, DATA_DIR
                
BATCH_SIZE = 128

def init_cluster():

    qdrant_client = QdrantClient(
        url=QDRANT_CLUSTER_URL,
        api_key=QDRANT_CLUSTER_TOKEN,
    )

    embeddings_path = os.path.join(DATA_DIR, 'embeddings.npy')
    embeddings = np.load(embeddings_path, allow_pickle=True)
    embedding_size = embeddings.shape[1]

    payloads_path = os.path.join(DATA_DIR, 'payloads.npy')
    payloads = np.load(payloads_path, allow_pickle=True)

    qdrant_client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=embedding_size, distance='Cosine'),
    )

    print('Uploading embeddings...')

    qdrant_client.upload_collection(
        collection_name=COLLECTION_NAME,
        vectors=embeddings,
        payload=payloads,
        ids=None,
        batch_size=BATCH_SIZE,
        parallel=2
    )

    print('Done uploading embeddings')
