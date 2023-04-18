import os

from data_init.env import read_env_vars

CODE_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.join(CODE_DIR, '../..')

read_env_vars(PROJECT_DIR, ['.env'])

DATA_DIR = os.path.normpath(os.path.join(PROJECT_DIR,\
            os.environ.get('DATA_DIR', '/data')))

IMG_DIR = os.path.normpath(os.path.join(DATA_DIR,\
            os.environ.get('IMG_SUB_DIR', '/imgs')))
HAIKU_DIR = os.path.normpath(os.path.join(DATA_DIR,\
            os.environ.get('HAIKU_SUB_DIR', '/haikus')))

HAIKU_CSV_URL = os.environ.get('HAIKU_CSV_URL')
IMG_CSV_URL = os.environ.get('IMG_CSV_URL')
