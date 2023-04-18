import os
import csv
import pickle
import urllib.request

from data_init.openimages_downloader import download_all_images

from data_init.config import DATA_DIR, IMG_DIR, HAIKU_DIR,\
                             IMG_CSV_URL, HAIKU_CSV_URL


def create_imgs_list(csv_file: str, list_file: str, url_file: str, max_n: int):
    if not os.path.isfile(csv_file): return
    if os.path.isfile(list_file): return
    if os.path.isfile(url_file): os.remove(url_file)

    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        with open(list_file, 'w', newline='') as listfile,\
             open(url_file, 'w', newline='') as urlfile:
            list_writer = csv.writer(listfile, delimiter=',')
            url_writer = csv.writer(urlfile, delimiter=',')

            for i, row in enumerate(reader):
                if i == 0: continue
                if i > max_n: break
                list_writer.writerow([row[1]+'/'+row[0]])
                url_writer.writerow([row[10] if row[10] else row[2]])


def create_haiku_json(csv_file: str, pkl_file: str):
    if not os.path.isfile(csv_file): return
    if os.path.isfile(pkl_file): return

    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        with open(pkl_file, 'wb') as pklfile:
            pickle.dump([[s.strip(' .-') for s in row[:3]]\
                        for row in reader], pklfile)


def download_haikus():
    if not os.path.isdir(DATA_DIR): os.mkdir(DATA_DIR)
    if not os.path.isdir(HAIKU_DIR): os.mkdir(HAIKU_DIR)

    haiku_csv = os.path.join(DATA_DIR, "haikus.csv")
    haiku_pkl = os.path.join(HAIKU_DIR, "haikus.pkl")

    if not os.path.isfile(haiku_csv):
        urllib.request.urlretrieve(HAIKU_CSV_URL, haiku_csv)

    create_haiku_json(haiku_csv, haiku_pkl)


def download_imgs(max_n: int):
    if not os.path.isdir(DATA_DIR): os.mkdir(DATA_DIR)
    if not os.path.isdir(IMG_DIR): os.mkdir(IMG_DIR)

    imgs_csv = os.path.join(DATA_DIR, "imgs.csv")
    imgs_list = os.path.join(DATA_DIR, "imgs.list")
    url_list = os.path.join(DATA_DIR, "urls.list")

    if not os.path.isfile(imgs_csv):
        urllib.request.urlretrieve(IMG_CSV_URL, imgs_csv)

    create_imgs_list(imgs_csv, imgs_list, url_list, max_n)

    if imgs_list and len(os.listdir(IMG_DIR)) == 0:
        download_all_images({'download_folder': IMG_DIR,\
                             'image_list': img_list_file,\
                             'num_processes': 5 })
