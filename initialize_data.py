import os
import argparse

from data_init.download import download_haikus, download_imgs
from data_init.embed import embed_haikus, embed_imgs
from data_init.upload import upload_haiku_embeddings, upload_img_embeddings

BASE_DIR = os.path.dirname(__file__)


def read_secrets(secret_file):

    if not os.path.isfile(secret_file):
        print('Could not read secrets file ' + secret_file + \
              '. File does not exist.')
        return

    print('Reading secrets file ' + secret_file)

    lines = []
    with open(secret_file, 'r') as file:
        lines += file.readlines()

    kvps = [line.strip().split('=') for line in lines\
            if not (line.startswith('#') or line.isspace())]

    secrets = {}
    for key, value in kvps:
        if key in ['QDRANT_CLUSTER_URL', 'QDRANT_CLUSTER_TOKEN']:
            secrets[key] = value

    if not secrets['QDRANT_CLUSTER_URL']:
        print('QDRANT_CLUSTER_URL could not be read from file ' + secret_file)

    if not secrets['QDRANT_CLUSTER_TOKEN']:
        print('QDRANT_CLUSTER_TOKEN could not be read from file ' + secret_file)

    return secrets


def initilize_data(args):

    data_dir = args['data_dir']
    if not os.path.isabs(data_dir):
        data_dir = os.path.join(BASE_DIR, data_dir)

    print('Initializing data using directory ' + data_dir)

    secret_file = args['secret_file']
    if not os.path.isabs(secret_file):
        secret_file = os.path.join(BASE_DIR, secret_file)

    img_collection_name = args['img_collection']
    haiku_collection_name = args['haiku_collection']

    max_imgs = args['max_imgs']
    max_haiku = args['max_haiku']

    download = args['download']
    embed = args['embed']
    upload = args['upload']

    only_imgs = args['only_imgs']
    only_haiku = args['only_haiku']

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if download:
        if not only_imgs:
            download_haikus(data_dir, max_haiku)
        if not only_haiku:
            download_imgs(data_dir, max_imgs)

    if embed:
        if not only_imgs:
            embed_haikus(data_dir, max_haiku)
        if not only_haiku:
            embed_imgs(data_dir, max_imgs)

    if upload:
        secrets = read_secrets(secret_file)
        if not only_imgs:
            upload_haiku_embeddings(data_dir, haiku_collection_name, secrets, max_haiku)
        if not only_haiku:
            upload_img_embeddings(data_dir, img_collection_name, secrets, max_imgs)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '--data_dir',
        type=str,
        default='data/',
        help='Data will be stored inside this directory')

    parser.add_argument(
        '--img_collection',
        type=str,
        default='images',
        help='Name of the image collection on the qdrant cluster')

    parser.add_argument(
        '--haiku_collection',
        type=str,
        default='haikus',
        help='Name of the haiku collection on the qdrant cluster')

    parser.add_argument(
        '--secret_file',
        type=str,
        default='secrets.env',
        help='File name (plus path) of the .env-file specifying the secret' + \
             'environment variables QDRANT_CLUSTER_URL and QDRANT_CLUSTER_TOKEN')

    parser.add_argument(
        '--max_imgs',
        type=int,
        default=5000,
        help='Maximum number of images to be processed')

    parser.add_argument(
       '--max_haiku',
       type=int,
       default=-1,
       help='Maximum number of haiku to be processed')

    parser.add_argument(
        '--no_download',
        dest='download',
        action='store_false',
        help='Downloading of data will be skipped')
    parser.set_defaults(download=True)

    parser.add_argument(
        '--no_embedding',
        dest='embed',
        action='store_false',
        help='Embedding of data will be skipped')
    parser.set_defaults(embed=True)

    parser.add_argument(
        '--no_upload',
        dest='upload',
        action='store_false',
        help='Uploading of embeddings will be skipped')
    parser.set_defaults(upload=True)

    parser.add_argument(
        '--only_haiku',
        action='store_true',
        default=False,
        help='Only handle haiku')

    parser.add_argument(
        '--only_imgs',
        action='store_true',
        default=False,
        help='Only handle images')

    initilize_data(vars(parser.parse_args()))
