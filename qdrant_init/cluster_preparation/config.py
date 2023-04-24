import os

from cluster_preparation.env import read_env_vars

CODE_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.join(CODE_DIR, '../..')

read_env_vars(PROJECT_DIR, ['.env', 'secrets.env'])

DATA_DIR = os.path.normpath(os.path.join(PROJECT_DIR,\
            os.environ.get('DATA_DIR', '/data')))

IMG_DIR = os.path.normpath(os.path.join(DATA_DIR,\
            os.environ.get('IMG_SUB_DIR', '/imgs')))
HAIKU_DIR = os.path.normpath(os.path.join(DATA_DIR,\
            os.environ.get('HAIKU_SUB_DIR', '/haikus')))

QDRANT_CLUSTER_URL = os.environ.get('QDRANT_CLUSTER_URL')
QDRANT_CLUSTER_TOKEN = os.environ.get('QDRANT_CLUSTER_TOKEN')

IMG_COLLECTION_NAME = os.environ.get('IMG_COLLECTION_NAME')
HAIKU_COLLECTION_NAME = os.environ.get('HAIKU_COLLECTION_NAME')
