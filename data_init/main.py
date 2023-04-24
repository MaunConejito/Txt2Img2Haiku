import pickle
from data_init.download import download_haikus, download_imgs

if __name__ == "__main__":
    download_haikus()
    download_imgs(max_n = 5000)
