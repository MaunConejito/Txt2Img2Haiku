import os
import numpy as np

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams

from cluster_preparation.config import QDRANT_CLUSTER_URL,\
                QDRANT_CLUSTER_TOKEN, IMG_COLLECTION_NAME,\
                HAIKU_COLLECTION_NAME, DATA_DIR, IMG_DIR, HAIKU_DIR

BATCH_SIZE = 128


def init_cluster():
    init_collection(IMG_COLLECTION_NAME, IMG_DIR)
    #init_collection(HAIKU_COLLECTION_NAME, HAIKU_DIR)


def init_collection(name: str, embedding_dir: str):

    qdrant_client = QdrantClient(
        url=QDRANT_CLUSTER_URL,
        api_key=QDRANT_CLUSTER_TOKEN,
    )

    embeddings_path = os.path.join(embedding_dir, 'embeddings.npy')
    embeddings = np.load(embeddings_path, allow_pickle=True)
    embedding_size = embeddings.shape[1]

    payloads_path = os.path.join(embedding_dir, 'payloads.npy')
    payloads = np.load(payloads_path, allow_pickle=True)

    print('Creating collection \"{}\" ...'.format(name))

    qdrant_client.recreate_collection(
        collection_name=name,
        vectors_config=VectorParams(size=embedding_size, distance='Cosine'),
    )

    print('Uploading embeddings ...')

    qdrant_client.upload_collection(
        collection_name=name,
        vectors=embeddings,
        payload=payloads,
        ids=None,
        batch_size=BATCH_SIZE,
        parallel=2
    )

    print('Done uploading embeddings')
