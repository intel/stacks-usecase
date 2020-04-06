#!/usr/bin/env python

"""train a UNET segmentation model using ICH physionet data."""
import pathlib

import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import Input, Model

import losses
from classic_unet import model as default_unet
from custom_unet import unet_model as custom_unet
from local import physionet_preprocess as prep
from utils import data_loader, helper


def train_unet(num_epochs=10, test_split=0.2, custom=False):

    # call data using the prepd data
    data_generator = data_loader.cloud_generator(test_split=test_split)
    epoch_length = data_loader.get_data_length(test_split=test_split)

    # use default sparse crossentropy loss
    dice_loss, dice_bce_loss = False, False

    if not (dice_loss or dice_bce_loss):
        print("using bce loss")
        loss = tf.keras.losses.binary_crossentropy
        metrics = ["accuracy"]
    elif dice_loss:
        print("using dice loss")
        loss = losses.dice_loss
        metrics = [losses.dice_coef]
    else:
        print("using combined dice, bce loss")
        loss = losses.dice_bce_loss
        metrics = [losses.dice_coef]

    # instantiate a custom model
    if custom:
        model = custom_unet()
        print("using custom unet arch.")
    else:
        model = default_unet()
        print("using default unet arch.")

    model.compile(optimizer="adam", loss=loss, metrics=metrics)
    callbacks = [
        tf.keras.callbacks.EarlyStopping(patience=10, verbose=1),
        tf.keras.callbacks.ReduceLROnPlateau(
            factor=0.1, patience=5, min_lr=0.0001, verbose=1
        ),
        tf.keras.callbacks.CSVLogger("training.log", append=False),
    ]
    model_history = model.fit(
        data_generator,
        epochs=num_epochs,
        steps_per_epoch=epoch_length,
        callbacks=callbacks,
    )

    train_loss = model_history.history["loss"]
    # val_loss = model_history.history["val_loss"]

    # Save model
    helper.save_unet(model=model, history=model_history)
    helper.save_unet(model=model, history=model_history, checkpoint=False)


def main():
    train_unet()


if __name__ == "__main__":
    main()
