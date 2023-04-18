import os
import shutil
import numpy as np
import pickle
from PIL import Image

from sentence_transformers import SentenceTransformer

from cluster_preparation.config import DATA_DIR, IMG_DIR,\
                                       HAIKU_DIR

BATCH_SIZE = 128

def create_embeddings():
    create_img_embeddings()
    create_haiku_embeddings()

def create_img_embeddings():
    embedding_file = os.path.join(IMG_DIR, 'embeddings.npy')
    payload_file = os.path.join(IMG_DIR, 'payloads.npy')

    if not os.path.isdir(IMG_DIR): return
    if os.path.isfile(embedding_file) and\
       os.path.isfile(payload_file):
        return
    else:
       if os.path.isfile(embedding_file): os.remove(embedding_file);
       if os.path.isfile(payload_file): os.remove(payload_file);

    print('Creating image-embeddings...')
    img_model = SentenceTransformer('clip-ViT-B-32')

    embeddings = []
    payloads = []
    batch = []
    batch_count = 0

    for img in os.listdir(IMG_DIR):
        batch.append(img)
        if len(batch) >= BATCH_SIZE:
            batch_count += 1
            imgs = [Image.open(os.path.join(IMG_DIR, img))\
                    for img in batch]
            embeddings.append(img_model.encode(imgs))
            payloads.append([{'fileName': img} for img in batch])
            batch = []
            print('Processed images: {}'\
                    .format(batch_count * BATCH_SIZE))

    if len(batch) >= 0:
        imgs = [Image.open(os.path.join(IMG_DIR, img))\
                for img in batch]
        embeddings.append(img_model.encode(imgs))
        payloads.append([{'fileName': img} for img in batch])

    embeddings = np.concatenate(embeddings)
    payloads = np.concatenate(payloads)

    np.save(embedding_file, embeddings, allow_pickle=True)
    np.save(payload_file, payloads, allow_pickle=True)


def create_haiku_embeddings():
    embedding_file = os.path.join(HAIKU_DIR, 'embeddings.npy')
    payload_file = os.path.join(HAIKU_DIR, 'payloads.npy')
    haiku_file = os.path.join(HAIKU_DIR, 'haikus.pkl')

    if not os.path.isfile(haiku_file): return
    if os.path.isfile(embedding_file) and\
       os.path.isfile(payload_file):
        return
    else:
       if os.path.isfile(embedding_file): os.remove(embedding_file);
       if os.path.isfile(payload_file): os.remove(payload_file);

    print('Creating haiku-embeddings...')
    text_model = SentenceTransformer(\
            'sentence-transformers/clip-ViT-B-32-multilingual-v1')

    embeddings = []
    payloads = []
    batch = []
    batch_count = 0

    with open(haiku_file, "rb") as f:
        haiku_list = pickle.load(f)

    for lines in haiku_list:
        batch.append(lines)
        if len(batch) >= BATCH_SIZE:
            batch_count += 1
            haikus = [' - '.join(lines) for lines in batch]
            embeddings.append(text_model.encode(haikus))
            payloads.append([{'lines': lines} for lines in batch])
            batch = []
            print('Processed haikus: {}'\
                    .format(batch_count * BATCH_SIZE))

    if len(batch) >= 0:
        haikus = [' - '.join(lines) for lines in batch]
        embeddings.append(img_model.encode(haikus))
        payloads.append([{'lines': lines} for lines in batch])

    embeddings = np.concatenate(embeddings)
    payloads = np.concatenate(payloads)

    np.save(embedding_file, embeddings, allow_pickle=True)
    np.save(payload_file, payloads, allow_pickle=True)
