#!/usr/bin/env python
import tarfile
import requests

try:
    from scripts.helper import get_directory
except ModuleNotFoundError:
    from helper import get_directory

url = "https://people.eecs.berkeley.edu/~tinghuiz/projects/pix2pix/datasets/facades.tar.gz"
dataset = "facades.tar.gz"


def download(url, dataset):
    """
    Download data from 'url'. Assumes data is in tar file and extracts it.
    """
    print("Downloading data")
    r = requests.get(url, allow_redirects=True)
    data_file_path = get_directory() + "/data/raw/"
    open(data_file_path + dataset, "wb").write(r.content)
    tar = tarfile.open(data_file_path + dataset)
    tar.extractall(path=data_file_path)
    tar.close()
    return True


if __name__ == "__main__":
    download(url, dataset)
