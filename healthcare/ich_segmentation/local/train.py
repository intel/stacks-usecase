"""train a UNET segmentation model using ICH physionet data."""
import pathlib

import matplotlib.pyplot as plt
import tensorflow as tf

import losses
from classic_unet import model as default_unet
from custom_unet import unet_model as custom_unet
from local import physionet_preprocess as prep
from utils import helper


def train_unet(num_epochs=10, batch_size=32, val_splits=5, custom=False):

    # use default sparse crossentropy loss
    dice_loss, dice_bce_loss = 0, 0

    # run preprocess and save input and label pngs
    data_preprocess = prep.ICHDataPreprocess()
    dataset, labels = data_preprocess.preprocess()

    # call a TF.data.Data generator using the prepd data
    data_gen = prep.ICHDataGenerator(dataset, labels)
    train_img_label, test_img_label, train_len, test_len = data_gen.test_train_data()

    STEPS_PER_EPOCH = train_len // batch_size
    VALIDATION_STEPS = test_len // batch_size // val_splits
    # shuffle buffer size, here the entire training set is used
    # if training fails, try reducing the BUFFER_SIZE
    BUFFER_SIZE = 100  # train_len

    train_dataset = train_img_label.batch(batch_size).repeat()
    train_dataset = train_dataset.prefetch(buffer_size=128)
    test_dataset = test_img_label.batch(batch_size)

    if not (dice_loss or dice_bce_loss):
        print("using bce loss")
        loss = losses.bce_loss
        metrics = ["BinaryAccuracy"]
    elif dice_loss:
        print("using dice loss")
        loss = losses.dice_loss
        metrics = [losses.dice_coef]
    else:
        print("using combined dice bce loss")
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
        tf.keras.callbacks.TensorBoard("logs"),
        tf.keras.callbacks.CSVLogger("logs/training.log", append=True),
        tf.keras.callbacks.ModelCheckpoint(
            monitor="val_loss", filepath="models/best_model.hdf5", save_best_only=True
        ),
    ]
    model_history = model.fit(
        train_dataset,
        epochs=num_epochs,
        callbacks=callbacks,
        steps_per_epoch=STEPS_PER_EPOCH,
        validation_steps=VALIDATION_STEPS,
        validation_data=test_dataset,
    )

    train_loss = model_history.history["loss"]
    val_loss = model_history.history["val_loss"]

    # Save model
    helper.save_unet(model=model, history=model_history)
    helper.save_unet(model=model, history=model_history, checkpoint=False)


def main(
    num_epochs=10,
    batch_size=32,
    val_splits=5,
    load_mod=False,
    checkpoint=False,
    custom=False,
):
    train_unet(num_epochs=10, batch_size=32, val_splits=5, custom=False)


if __name__ == "__main__":
    main()
