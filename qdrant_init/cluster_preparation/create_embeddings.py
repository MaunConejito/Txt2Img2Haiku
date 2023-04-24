import os
import shutil
import numpy as np
import pickle
from PIL import Image

from sentence_transformers import SentenceTransformer

from cluster_preparation.config import DATA_DIR, IMG_DIR,\
                                       HAIKU_DIR

IMG_BATCH_SIZE = 128
HAIKU_BATCH_SIZE = 128*8

def create_embeddings():
    create_img_embeddings()
    create_haiku_embeddings()

def create_img_embeddings():
    embedding_file = os.path.join(IMG_DIR, 'embeddings.npy')
    payload_file = os.path.join(IMG_DIR, 'payloads.npy')

    url_file = os.path.join(DATA_DIR, 'id_url_map.pkl')

    if not os.path.isfile(url_file): return
    if not os.path.isdir(IMG_DIR): return
    if os.path.isfile(embedding_file) and\
       os.path.isfile(payload_file):
        return
    else:
       if os.path.isfile(embedding_file): os.remove(embedding_file);
       if os.path.isfile(payload_file): os.remove(payload_file);

    print('Creating image-embeddings...')
    img_model = SentenceTransformer('clip-ViT-B-32')

    with open(url_file, 'rb') as pickle_file:
        id_url_map = pickle.load(pickle_file)

    embeddings = []
    payloads = []
    batch = []
    batch_count = 0

    n_total = len(id_url_map)
    for id, url in id_url_map.items():
        img = id + '.jpg'
        batch.append([img, url])
        if len(batch) >= IMG_BATCH_SIZE:
            batch_count += 1
            imgs = [Image.open(os.path.join(IMG_DIR, img))\
                    for img, _ in batch]
            embeddings.append(img_model.encode(imgs))
            payloads.append([{'url': url} for _, url in batch])
            batch = []
            print('Processed images: {} of {}'\
                    .format(batch_count * IMG_BATCH_SIZE, n_total))

    if len(batch) >= 0:
        imgs = [Image.open(os.path.join(IMG_DIR, img))\
                for img, _ in batch]
        embeddings.append(img_model.encode(imgs))
        payloads.append([{'url': url} for _, url in batch])
        print('Processed images: {} of {}'.format(n_total, n_total))

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

    n_total = len(haiku_list)
    for lines in haiku_list:
        batch.append(lines)
        if len(batch) >= HAIKU_BATCH_SIZE:
            batch_count += 1
            haikus = [' - '.join(lines) for lines in batch]
            embeddings.append(text_model.encode(haikus))
            payloads.append([{'lines': lines} for lines in batch])
            batch = []
            print('Processed haikus: {} of {}'\
                    .format(batch_count * HAIKU_BATCH_SIZE, n_total))

    if len(batch) >= 0:
        haikus = [' - '.join(lines) for lines in batch]
        embeddings.append(text_model.encode(haikus))
        payloads.append([{'lines': lines} for lines in batch])
        print('Processed haikus: {} of {}'.format(n_total, n_total))

    embeddings = np.concatenate(embeddings)
    payloads = np.concatenate(payloads)

    np.save(embedding_file, embeddings, allow_pickle=True)
    np.save(payload_file, payloads, allow_pickle=True)
