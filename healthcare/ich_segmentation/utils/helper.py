# Helper Functions

import datetime
import glob
import os
import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

from os.path import abspath, dirname

import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.models import Model, load_model
from classic_unet import unet_model


def get_directory():
    """
    Get the name of home directory of usecase. Use the home directory for file
    path construction to avoid relative path errors
    """
    home_dir = dirname(dirname(abspath(__file__)))  # call dirname twice to get parent dir
    return home_dir


def save_unet(model, history, checkpoint=True):
    """Save the trained model. Only for use in local training. """
    home_dir = get_directory()
    if checkpoint:
        try:
            key = "acc"
            last = len(history.history[key])
        except KeyError:
            key = "accuracy"
            last = len(history.history[key])
        acc = history.history[key][last - 1]
        model.save(
            home_dir
            + "/models/checkpoints/unet-"
            + str(datetime.datetime.now()).replace(" ", "-")
            + "-acc-"
            + str(acc)
            + ".h5"
        )
    else:
        model.save(
            home_dir
            + "/models/unet.h5"
        )


def load_unet(checkpoint=False):
    """
    Return  unet model. Only for use in local training.
    checkpoint: True to return the latest ckeckpoint in models/,
        False to return a model named 'unet.h5' in models/
    """
    home_dir = get_directory()
    unet_names = glob.glob(os.path.join(home_dir, "models/checkpoints/unet-*.h5"))
    if checkpoint:
        try:
            unet_file = max(unet_names, key=os.path.getctime)
            unet_model = load_model(unet_file)
        except ValueError:
            print("Could not load checkpoint. Returning new model instead.")
            unet_model = unet_model()
    else:
        try:
            unet_model = load_model(os.path.join(home_dir, "models/unet.h5"))
        except ValueError:
            print("Could not load from 'models/unet.h5'. Returning new model instead.")
            unet_model = unet_model()
    return unet_model


def val_train_plot(epochs, train_loss, val_loss):
    """plot training and validation loss."""
    epochs = range(epochs) if not isinstance(epochs, list) else epochs
    plt.figure()
    plt.plot(epochs, train_loss, "r", label="Training loss")
    plt.plot(epochs, val_loss, "bo", label="Validation loss")
    plt.title("Training and Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss Value")
    plt.ylim([0, 1])
    plt.legend()
    plt.show()


def main():
    print(f"{__name__} ran\n")


if __name__ == "__main__":
    main()
