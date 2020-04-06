"""
Load data from a cassandra DB
"""
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

from cassandra.cluster import Cluster
import os, uuid, io
from math import floor
from PIL import Image
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split

from utils.helper import get_directory


def _convert_input(image):
    img = np.array(image) / 255
    img = img.astype("float32")
    img = np.reshape(img, (1,512,512,1))
    return img


def _convert_label(image):
    img = np.array(image) // 254
    img = img.astype("float32")
    img = np.reshape(img, (1,512,512,1))
    return img


def _return_input_and_label(rows):
    for file_row in rows:
        if file_row.is_label:
            label = Image.open(io.BytesIO(file_row.image_blob))
            label = _convert_input(label)
        else:
            in_img = Image.open(io.BytesIO(file_row.image_blob))
            in_img = _convert_label(in_img)
    return in_img, label

def _get_image_filenames(test_split=0.2):
    f_names_path = os.path.join(get_directory(), "ich_filenames.csv")
    f_names =  pd.read_csv(f_names_path, index_col=0)
    num_data = len(f_names.index)
    split = floor(num_data*(1-test_split))
    f_names = f_names.iloc[:split]
    return f_names


def get_data_length(test_split=0.2):
    f_names_path = os.path.join(get_directory(), "ich_filenames.csv")
    f_names =  pd.read_csv(f_names_path, index_col=0)
    num_data = len(f_names.index)
    split = floor(num_data*(1-test_split))
    return split


def cloud_generator(test_split=0.2):
    """
    Generator for cloud use.
    test_split: Percentage of data to reserve for testing.
    Return X, y (input image and label)
    """
    # retrieve raw data
    cluster = Cluster(['10.44.27.2'])
    session = cluster.connect('healthcare_keyspace_v2')
    f_names = _get_image_filenames(test_split=test_split)
    while True:
        for x in f_names.iloc:
            query = "SELECT image_blob, is_label FROM processed_data"
            query = query + " WHERE image_filename='" + x[0] + "'" + "ALLOW FILTERING"
            rows = session.execute(query)
            X, y = _return_input_and_label(rows)
            yield X, y

            
def main():
    return_train_test()


if __name__ == '__main__':
    main()
