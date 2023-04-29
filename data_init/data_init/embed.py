import os
import shutil
import numpy as np
import pickle
from PIL import Image

from sentence_transformers import SentenceTransformer

from data_init.config import IMG_SUB_DIR, HAIKU_SUB_DIR,\
                             IMG_MAP_FILE, IMG_STORAGE,\
                             HAIKU_STORAGE_FILE,\
                             IMG_EMBEDDING_FILE, IMG_PAYLOAD_FILE,\
                             HAIKU_EMBEDDING_FILE, HAIKU_PAYLOAD_FILE,\
                             IMG_BATCH_SIZE, HAIKU_BATCH_SIZE


def embed_imgs(data_dir: str, max_n: int):

    img_dir = os.path.join(data_dir, IMG_SUB_DIR)
    storage_dir = os.path.join(img_dir, IMG_STORAGE)
    embedding_file = os.path.join(img_dir, IMG_EMBEDDING_FILE)
    payload_file = os.path.join(img_dir, IMG_PAYLOAD_FILE)

    map_file = os.path.join(img_dir, IMG_MAP_FILE)

    if not os.path.isfile(map_file):
        print('Failed to embed images: map file ' + map_file + \
              ' does not exist.')
        return

    if not os.path.isdir(storage_dir):
        print('Failed to embed images: storage directory ' + storage_dir + \
              ' does not exist.')
        return

    print('Creating image embeddings ...')

    print('Loading model ...')
    img_model = SentenceTransformer('clip-ViT-B-32')

    with open(map_file, 'rb') as rfile:
        id_url_map = pickle.load(rfile)

    embeddings = []
    payloads = []
    batch = []
    batch_count = 0

    kvps = list(id_url_map.items())[:max_n] # actually wastes memory but easy to implement max_n
    n_total = len(kvps)
    for id, url in kvps:
        img = id + '.jpg'
        batch.append([img, url])
        if len(batch) >= IMG_BATCH_SIZE:
            batch_count += 1
            imgs = [Image.open(os.path.join(storage_dir, img))\
                    for img, _ in batch]
            embeddings.append(img_model.encode(imgs))
            payloads.append([{'url': url} for _, url in batch])
            batch = []
            print('Embedded images: {} of {}'\
                    .format(batch_count * IMG_BATCH_SIZE, n_total))

    if len(batch) > 0:
        imgs = [Image.open(os.path.join(storage_dir, img))\
                for img, _ in batch]
        embeddings.append(img_model.encode(imgs))
        payloads.append([{'url': url} for _, url in batch])
        print('Embedded images: {} of {}'.format(n_total, n_total))

    embeddings = np.concatenate(embeddings)
    payloads = np.concatenate(payloads)

    np.save(embedding_file, embeddings, allow_pickle=True)
    np.save(payload_file, payloads, allow_pickle=True)


def embed_haikus(data_dir: str, max_n: int):

    haiku_dir = os.path.join(data_dir, HAIKU_SUB_DIR)
    storage_file = os.path.join(haiku_dir, HAIKU_STORAGE_FILE)
    embedding_file = os.path.join(haiku_dir, HAIKU_EMBEDDING_FILE)
    payload_file = os.path.join(haiku_dir, HAIKU_PAYLOAD_FILE)

    if not os.path.isfile(storage_file):
        print('Failed to embed haiku: storage file ' + storage_file + \
              ' does not exist.')
        return

    print('Creating haiku embeddings ...')

    print('Loading model ...')
    text_model = SentenceTransformer(\
            'sentence-transformers/clip-ViT-B-32-multilingual-v1')

    embeddings = []
    payloads = []
    batch = []
    batch_count = 0

    with open(storage_file, 'rb') as f:
        haiku_list = pickle.load(f)[:max_n]

    n_total = len(haiku_list)
    for lines in haiku_list:
        batch.append(lines)
        if len(batch) >= HAIKU_BATCH_SIZE:
            batch_count += 1
            haikus = [' - '.join(lines) for lines in batch]
            embeddings.append(text_model.encode(haikus))
            payloads.append([{'lines': lines} for lines in batch])
            batch = []
            print('Embedded haiku: {} of {}'\
                    .format(batch_count * HAIKU_BATCH_SIZE, n_total))

    if len(batch) > 0:
        haikus = [' - '.join(lines) for lines in batch]
        embeddings.append(text_model.encode(haikus))
        payloads.append([{'lines': lines} for lines in batch])
        print('Embedded haiku: {} of {}'.format(n_total, n_total))

    embeddings = np.concatenate(embeddings)
    payloads = np.concatenate(payloads)

    np.save(embedding_file, embeddings, allow_pickle=True)
    np.save(payload_file, payloads, allow_pickle=True)
