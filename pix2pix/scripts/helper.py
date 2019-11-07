# Helper Functions

import datetime
import numpy as np
import random

import glob
from os.path import abspath, dirname
import psutil
import subprocess

from PIL import Image
from sklearn.preprocessing import normalize
from tensorflow.keras.models import Model


def get_cpuinfo():
    """return num of physical cores and sockets"""
    num_sockets = int(
        subprocess.check_output(
            "cat /proc/cpuinfo | grep 'physical id' | sort -u | wc -l", shell=True
        )
    )
    return psutil.cpu_count(logical=False), num_sockets


def get_directory():
    """
    Get the name of home directory of usecase. Use the home directory for file
    path construction.
    """
    home_dir = dirname(
        dirname(abspath(__file__))
    )  # call dirname twice to get parent dir
    return home_dir


def get_image_f_names(location):
    """ Return a list of file names for images"""
    f_names_list = []
    for f_name in glob.glob(location):
        f_names_list.append(f_name)
    return f_names_list


def reverse_norm(img, heigth=256, width=256, channels=3):
    """ Take a normalized output and return it to the 0-256 image range
    This function is hardcoded to receive an image normalized from -1 to 1"""
    if np.amin(img) < -1.003:
        raise ValueError("the normalized data contains values less than -1.003")
    if np.amax(img) > 1.003:
        raise ValueError("The normalized data contains values greater than 1.003")
    img = np.add(img, 1) * 128
    img = img.astype(np.uint8)
    return img


def norm_data(data):
    """ Inputs
    data - a list of numpy arrays representing images
    Normalize data between -1 and 1
    This is hardcoded for images of size 256 by 256"""
    return [x / 128 - 1 for x in data]  # data is now normalized from -1 to 1


def create_y_values_gen(size_batch=50):
    """return list of y values for generators"""
    home_dir = get_directory()
    num_abs_data = len(get_image_f_names(home_dir + "/data/tidy/input/*.jpg"))
    num_real_data = len(get_image_f_names(home_dir + "/data/tidy/real/*.jpg"))
    # numbers should match
    if num_abs_data != num_real_data:
        raise ValueError(
            "the number of abstract images (/data/tidy/input/) does not match the number of real data images (data/tidy/real/). These should be pairs."
        )
    y = []
    for _ in range(0, size_batch):
        y.append(np.zeros((16, 16, 1)))
    y = np.asarray(y)
    return y


def create_y_values_disc(size_batch=50):
    """return list of y values for combined discriminator with patches"""
    home_dir = get_directory()
    num_abs_data = len(get_image_f_names(home_dir + "/data/tidy/input/*.jpg"))
    num_real_data = len(get_image_f_names(home_dir + "/data/tidy/real/*.jpg"))
    if num_abs_data != num_real_data:  # numbers should match
        raise ValueError(
            "the number of abstract images (/data/tidy/input/) does not match the number of real data images (data/tidy/real/). These should be pairs."
        )
    y = []
    for x in range(0, size_batch):  # real data is labeled as ~0, generated data ~1
        lows = np.zeros(shape=(16, 16, 1))
        highs = np.ones(shape=(16, 16, 1))
        low_and_high = np.concatenate((lows, highs), axis=2)
        y.append(low_and_high)
    y = np.asarray(y)
    return y


def load_data(normalize=True, batch=True, size_batch=50):
    """Load X (input) and y (real) images from disk, return normalized X and y
    Can return non normalized data for unit testing
    If batch=True, will return a small randomized batch instead of the full
    dataset. Useful for speeding up training."""
    home_dir = get_directory()
    # Get file names
    abstract_list = get_image_f_names(home_dir + "/data/tidy/input/*.jpg")
    real_list = get_image_f_names(home_dir + "/data/tidy/real/*.jpg")
    if not any([abstract_list, real_list]):
        raise ValueError(
            "Dataset missing, check to see if /data/tidy/ directory has image files."
        )
    # Create random batch
    if batch:
        abstract_list_batch = []
        real_list_batch = []
        rand_indices = random.sample(range(0, len(abstract_list)), size_batch)
        for i in rand_indices:
            abstract_list_batch.append(abstract_list[i])
            real_list_batch.append(real_list[i])
        abstract_list = abstract_list_batch
        real_list = real_list_batch
    # load images and transform then into numpy array
    if normalize:
        abs_data = norm_data([np.array(Image.open(x)) for x in abstract_list])
        real_data = norm_data([np.array(Image.open(x)) for x in real_list])
    else:
        abs_data = [np.array(Image.open(x)) for x in abstract_list]
        real_data = [np.array(Image.open(x)) for x in real_list]
    return abs_data, real_data


def checkpoint_disc(model, history):
    """Saves a checkpoint of the discriminator.
    Inputs:
     - model: the model to be saved
     - history: history object returned from training (.fit)"""
    home_dir = get_directory()
    try:
        key = "acc"
        last = len(history.history[key])
    except KeyError:
        key = "accuracy"
        last = len(history.history[key])
    acc = history.history[key][last - 1]
    model.save(
        home_dir
        + "/models/checkpoints/discriminator-"
        + str(datetime.datetime.now()).replace(" ", "-")
        + "-acc-"
        + str(acc)
        + ".h5"
    )


def checkpoint_gen(model, history):
    """Saves a checkpoint of the discriminator.
    Inputs:
     - model: the model to be saved
     - history: history object returned from training (.fit)"""
    home_dir = get_directory()
    try:
        key = "Discriminator_acc"
        last = len(history.history[key])
    except KeyError:
        key = "Discriminator_accuracy"
        last = len(history.history[key])
    acc = history.history[key][last - 1]
    model.save(
        home_dir
        + "/models/checkpoints/generator-"
        + str(datetime.datetime.now()).replace(" ", "-")
        + "-acc-"
        + str(acc)
        + ".h5"
    )


def checkpoint_image(gen_model):
    """Saves the generated, real, and abstract image at a checkpoint"""
    # load data
    abs_data, real_data = load_data(batch=False)
    IMAGE_NUM = 3
    # predict
    result = gen_model.predict(abs_data[IMAGE_NUM].reshape(1, 256, 256, 3))
    # reverse norm the images
    result = reverse_norm(result[0])
    abs_0 = reverse_norm(abs_data[IMAGE_NUM])
    real_0 = reverse_norm(real_data[IMAGE_NUM])
    # stack three images and display
    home_dir = get_directory()
    Image.fromarray(np.hstack((np.hstack((result, real_0)), abs_0)), "RGB").save(
        home_dir + "/models/img_ckpts/" + str(datetime.datetime.now()) + ".jpg"
    )
    return True
