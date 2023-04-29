import os
import csv
import pickle
import urllib.request

from data_init.openimages_downloader import download_all_images

from data_init.config import IMG_SUB_DIR, HAIKU_SUB_DIR,\
                             IMG_CSV_URL, HAIKU_CSV_URL,\
                             IMG_MAP_FILE, IMG_STORAGE,\
                             HAIKU_STORAGE_FILE

IMG_CSV_FILE = './imgs.csv'
IMG_LIST_FILE = './imgs.list'
HAIKU_CSV_FILE = './haiku.csv'


def create_imgs_list(csv_file: str, list_file: str, map_file: str, max_n: int):

    if not os.path.isfile(csv_file):
        print('Failed to create image list file: csv file ' + csv_file + \
              ' does not exist.')
        return

    url_dict = {}

    with open(csv_file, newline='') as rfile:
        reader = csv.reader(rfile, delimiter=',')

        with open(list_file, 'w', newline='') as wfile:
            writer = csv.writer(wfile, delimiter=',')

            for i, row in enumerate(reader):
                if i == 0: continue
                if max_n >= 0 and i > max_n: break
                writer.writerow([row[1]+'/'+row[0]])
                url_dict[row[0]] = row[10] if row[10] else row[2]

    with open(map_file, 'wb') as wfile:
        pickle.dump(url_dict, wfile)


def create_haiku_json(csv_file: str, storage_file: str, max_n: int):

    if not os.path.isfile(csv_file):
        print('Failed to create haiku json: csv file ' + csv_file + \
              ' does not exist.')
        return

    with open(csv_file, newline='') as rfile:
        reader = csv.reader(rfile, delimiter=',')

        with open(storage_file, 'wb') as wfile:
            pickle.dump([[s.strip(' .-') for s in row[:3]]\
                        for row in reader][:max_n], wfile)


def download_haikus(data_dir: str, max_n: int):

    haiku_dir = os.path.join(data_dir, HAIKU_SUB_DIR)
    if not os.path.isdir(haiku_dir):
        os.mkdir(haiku_dir)

    haiku_csv = os.path.join(haiku_dir, HAIKU_CSV_FILE)
    haiku_storage_file = os.path.join(haiku_dir, HAIKU_STORAGE_FILE)

    if not os.path.isfile(haiku_csv):
        print('Downloading haiku csv file ...')
        urllib.request.urlretrieve(HAIKU_CSV_URL, haiku_csv)

    create_haiku_json(haiku_csv, haiku_storage_file, max_n)


def download_imgs(data_dir: str, max_n: int):

    img_dir = os.path.join(data_dir, IMG_SUB_DIR)
    if not os.path.isdir(img_dir):
        os.mkdir(img_dir)

    img_csv = os.path.join(img_dir, IMG_CSV_FILE)
    img_list = os.path.join(img_dir, IMG_LIST_FILE)
    map_file = os.path.join(img_dir, IMG_MAP_FILE)
    storage_dir = os.path.join(img_dir, IMG_STORAGE)

    if not os.path.isfile(img_csv):
        print('Downloading image csv file ...')
        urllib.request.urlretrieve(IMG_CSV_URL, img_csv)

    create_imgs_list(img_csv, img_list, map_file, max_n)

    if not os.path.isdir(storage_dir):
        os.mkdir(storage_dir)

    if os.path.isfile(img_list):
        download_all_images({'download_folder': storage_dir,\
                             'image_list': img_list,\
                             'num_processes': 5 })
