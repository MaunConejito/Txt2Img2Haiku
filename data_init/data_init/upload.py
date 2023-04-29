import os
import numpy as np
from typing import Dict as dict

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams

from data_init.config import IMG_SUB_DIR, HAIKU_SUB_DIR,\
                             IMG_EMBEDDING_FILE, IMG_PAYLOAD_FILE,\
                             HAIKU_EMBEDDING_FILE, HAIKU_PAYLOAD_FILE,\
                             UPLOAD_BATCH_SIZE


def init_collection(name: str, embedding_file: str, payload_file: str ,\
                    secrets: dict[str, str], max_n: int):

    qdrant_client = QdrantClient(
        url=secrets['QDRANT_CLUSTER_URL'],
        api_key=secrets['QDRANT_CLUSTER_TOKEN'],
    )

    embeddings = np.load(embedding_file, allow_pickle=True)
    embedding_size = embeddings.shape[1]

    payloads = np.load(payload_file, allow_pickle=True)

    print('Creating collection \"{}\" ...'.format(name))

    qdrant_client.recreate_collection(
        collection_name=name,
        vectors_config=VectorParams(size=embedding_size, distance='Cosine'),
    )

    print('Uploading embeddings ...')

    qdrant_client.upload_collection(
        collection_name=name,
        vectors=embeddings[:max_n],
        payload=payloads[:max_n],
        ids=None,
        batch_size=UPLOAD_BATCH_SIZE,
        parallel=1 # got warnings when using parallelization
    )

    print('Done uploading embeddings')


def upload_haiku_embeddings(data_dir: str, collection_name: str, secrets: dict[str, str], max_n: int):

    haiku_dir = os.path.join(data_dir, HAIKU_SUB_DIR)
    embedding_file = os.path.join(haiku_dir, HAIKU_EMBEDDING_FILE)
    payload_file = os.path.join(haiku_dir, HAIKU_PAYLOAD_FILE)

    if not os.path.isfile(embedding_file):
        print('Failed to initialize haiku collection: embedding file ' + \
              storage_file + ' does not exist.')
        return

    if not os.path.isfile(payload_file):
        print('Failed to initialize haiku collection: payload file ' + \
              payload_file + ' does not exist.')
        return

    if (collection_name):
        init_collection(collection_name, embedding_file, payload_file, secrets, max_n)
    else:
        print('Failed to initialize haiku collection: ' + \
              'collection name is empty.')

def upload_img_embeddings(data_dir: str, collection_name: str, secrets: dict[str, str], max_n: int):

  img_dir = os.path.join(data_dir, IMG_SUB_DIR)
  embedding_file = os.path.join(img_dir, IMG_EMBEDDING_FILE)
  payload_file = os.path.join(img_dir, IMG_PAYLOAD_FILE)

  if not os.path.isfile(embedding_file):
      print('Failed to initialize ig collection: embedding file ' + \
            storage_file + ' does not exist.')
      return

  if not os.path.isfile(payload_file):
      print('Failed to initialize img collection: payload file ' + \
            payload_file + ' does not exist.')
      return

  if (collection_name):
      init_collection(collection_name, embedding_file, payload_file, secrets, max_n)
  else:
      print('Failed to initialize img collection: ' + \
            'collection name is empty.')
