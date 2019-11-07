###########################################################
# Pix2pix keras/tensorflow implementation
###########################################################

import argparse
import os
import glob

import numpy as np
import tensorflow as tf
from tensorflow.keras import backend
from tensorflow.keras.initializers import RandomNormal
from tensorflow.keras.layers import (
    BatchNormalization,
    Concatenate,
    Conv2D,
    Conv2DTranspose,
    Dropout,
    Input,
    LeakyReLU,
)
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.optimizers import Adam

# Local helper functions
from scripts.helper import (
    checkpoint_image,
    checkpoint_disc,
    checkpoint_gen,
    create_y_values_disc,
    create_y_values_gen,
    get_directory,
    load_data,
    get_cpuinfo,
)

# debug - supressing tensorflow warnings
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# Constants
LEAKY_RELU_ALPHA = 0.2
FILTER = (4, 4)
STRIDE = (2, 2)
DROPOUT_RATE = 0.50  # 50%
IMAGE_SIZE = (256, 256, 3)
LEARNING_RATE_GEN = 0.0002
LEARNING_RATE_DISC = 0.0002

###########################################################
# Parse input arguments
###########################################################
parser = argparse.ArgumentParser()
parser.add_argument(
    "--model",
    choices=["continue", "checkpoint"],
    default="checkpoint",
    help="Your options are 'continue' and 'checkpoint'. \
            'Checkpoint' will load the latest checkpoint model \
            in pix2pix/models/checkpoints/ and 'continue' \
            will load models named 'discriminator_model.h5'\
            and 'generator_model.h5' in pix2pix/models/ ",
)
parser.add_argument(
    "--cycles",
    type=int,
    default=1000,
    help="One cycle is training the discriminator and \
            generator for 1 batch of loaded data.This \
            sets how many cycles are trained.",
)
parser.add_argument(
    "--size_batch",
    type=int,
    default=50,
    help="size_batch is how many samples are trained \
            on before switching between the generator \
            and discriminator training.",
)
parser.add_argument(
    "--check_freq",
    type=int,
    choices=[1000, 200, 100, 50, 20, 1],
    default=20,
    help="check_freq is how frequently checkpoints \
            will be taken.",
)
arguments = parser.parse_args()


###########################################################
# Layer Utility Functions
# functions that condense repeated keras layer calls
###########################################################
def conv_lb(prev_layer, num_filters, layer_name, pad="same", batch_norm=True):
    """
    conv_lb
    Condensing operations into new function for better readability
    performs a convolution, then batch normalization, then leakyReLU
    Input: single layer (prev_layer) along with constant parameters
    Output: single layer
    """
    weight_init = RandomNormal(stddev=0.02)
    new_layer = Conv2D(
        num_filters, FILTER, strides=STRIDE, padding=pad, kernel_initializer=weight_init
    )(prev_layer)
    if batch_norm:
        new_layer = BatchNormalization()(new_layer, training=True)
    new_layer = LeakyReLU(alpha=LEAKY_RELU_ALPHA, name=layer_name)(new_layer)
    return new_layer


def deconv_b(prev_layer, num_filters, batch_norm=True):
    """
    deconv_b
    Condensing operations into new function for better readability
    performs a convolution, then batch normalization
    Input: single layer (prev_layer) along with constant parameters
    Output: single layer
    """
    weight_init = RandomNormal(stddev=0.02)
    new_layer = Conv2DTranspose(
        num_filters,
        FILTER,
        strides=STRIDE,
        padding="same",
        activation="relu",
        kernel_initializer=weight_init,
    )(prev_layer)
    if batch_norm:
        new_layer = BatchNormalization()(new_layer, training=True)
    return new_layer


def concat_deconv(prev_layer, skip_layer, num_filters, batch_norm=True, dropout=True):
    """
    concat_deconv
    Condensing operations into new function for better readability
    Performs a deconvolution, then concatenates two layers,
    then batch normalization if batch_norm=True
    Input: two layers (prev_layer, skip_layer) along with constant parameters
    Output: single layer
    """
    weight_init = RandomNormal(stddev=0.02)
    new_layer = Conv2DTranspose(
        num_filters,
        FILTER,
        strides=STRIDE,
        padding="same",
        activation="relu",
        kernel_initializer=weight_init,
    )(prev_layer)
    new_layer = Concatenate()([skip_layer, new_layer])
    if batch_norm:
        new_layer = BatchNormalization()(new_layer, training=True)
    if dropout:
        new_layer = Dropout(rate=DROPOUT_RATE)(new_layer, training=True)
    return new_layer


###########################################################
# Generator, U-net
###########################################################
def generator(summary=False):
    """
    Generates image based on input. Uses a U-net.
    Training is focused on making the generator
    as good as possible, because the generator
    is used in inference.

    variable legend:
        e = encoder
        s = center layer
        d = decoder
        # (ie 1,2,3,etc) = layer number
        a = activation
        b = batch normalization
        c = a concatenated layer
    So d3ab is the layer 3 decoder that has gone
    through activation and batch normalization.
    """
    # -----------------------------------------------------------
    # Encoder
    input_tensor = Input(shape=IMAGE_SIZE)
    e1a = conv_lb(input_tensor, 64, layer_name="layer_1", batch_norm=False)
    e2ba = conv_lb(e1a, 128, layer_name="layer_2")
    e3ba = conv_lb(e2ba, 256, layer_name="layer_3")
    e4ba = conv_lb(e3ba, 512, layer_name="layer_4")
    e5ba = conv_lb(e4ba, 512, layer_name="layer_5")
    e6ba = conv_lb(e5ba, 512, layer_name="layer_6")
    e7ba = conv_lb(e6ba, 512, layer_name="layer_7")
    # -----------------------------------------------------------
    # Center layer
    s8ba = conv_lb(e7ba, 512, layer_name="middle_layer", batch_norm=False)
    # -----------------------------------------------------------
    # Decoder
    d9cba = concat_deconv(s8ba, e7ba, 512)
    d10cba = concat_deconv(d9cba, e6ba, 512)
    d11cba = concat_deconv(d10cba, e5ba, 512)
    d12cba = concat_deconv(d11cba, e4ba, 512, dropout=False)
    d13cba = concat_deconv(d12cba, e3ba, 256, dropout=False)
    d14cba = concat_deconv(d13cba, e2ba, 128, dropout=False)
    d15cba = concat_deconv(d14cba, e1a, 64, dropout=False)
    d16ba = Conv2DTranspose(
        3,
        FILTER,
        strides=STRIDE,
        padding="same",
        activation="tanh",
        kernel_initializer=RandomNormal(stddev=0.02),
    )(d15cba)
    # Define generator model
    gen_model = Model(input_tensor, d16ba, name="Generator")
    if summary:
        gen_model.summary()
    return gen_model


###########################################################
# Discriminator
###########################################################
def discriminator(summary=False):
    """
    Decides whether an image is real or generated. Used in
    training the generator.
    """
    input_img = Input(shape=IMAGE_SIZE)  # image put into generator
    unknown_img = Input(shape=IMAGE_SIZE)  # either real image or generated image
    weight_init = RandomNormal(stddev=0.02)

    input_tensor = Concatenate()([input_img, unknown_img])
    d = conv_lb(input_tensor, 64, layer_name="layer_1", batch_norm=False)
    d = conv_lb(d, 128, layer_name="layer_2")
    d = conv_lb(d, 256, layer_name="layer_3")
    d = conv_lb(d, 512, layer_name="layer_4")
    d = Conv2D(
        1,
        FILTER,
        padding="same",
        kernel_initializer=weight_init,
        activation="sigmoid",
        name="layer_6",
    )(d)

    # Define discriminator model
    dis_model = Model(inputs=[input_img, unknown_img], outputs=d, name="Discriminator")
    if summary:
        dis_model.summary()
    return dis_model


###########################################################
# General Utility Functions
###########################################################
def load_disc_gen():
    """ load models for training. Separate from 'load_model'.
    Returns Discriminator, Generator"""
    home_dir = get_directory()
    generators = glob.glob(os.path.join(home_dir, "models/checkpoints/generator-*.h5"))
    discriminators = glob.glob(
        os.path.join(home_dir, "models/checkpoints/discriminator-*.h5")
    )
    try:
        gen_model_file = max(generators, key=os.path.getctime)
        gen_model = load_model(gen_model_file)
    except ValueError:
        gen_model = generator()
    try:
        disc_model_file = max(discriminators, key=os.path.getctime)
        disc_model = load_model(disc_model_file)
    except ValueError:
        disc_model = discriminator()

    return disc_model, gen_model

def cpu_config(first=False):
    # intel optimizations
    num_cores, num_sockets = get_cpuinfo()
    if first:
        print("system info::")
        print("Number of physical cores:: ", num_cores)
        print("Number of sockets::", num_sockets)
    backend.set_session(
        tf.Session(
            config=tf.ConfigProto(
                intra_op_parallelism_threads=num_cores,
                inter_op_parallelism_threads=num_sockets,
            )
        )
    )
###########################################################
# Training
###########################################################
def train(model="checkpoint", cycles=1000, size_batch=50, checkpoint=20):
    cpu_config(first=True)
    # --------------------------------------
    # Load models and data
    # If generator and discriminator models already exist,
    # load them. Otherwise, make them.
    home_dir = get_directory()
    if model == "continue":
        try:
            gen_model = load_model(home_dir + "/models/generator_model.h5")
        except ValueError:
            gen_model = generator()
        try:
            disc_model = load_model(home_dir + "/models/discriminator_model.h5")
        except ValueError:
            disc_model = discriminator()
    else:
        disc_model, gen_model = load_disc_gen()

    for i in range(0, int(cycles / checkpoint)):
        # --------------------------------------
        # define generator training models
        input_gen = Input(shape=IMAGE_SIZE, name="Input_abstract_gen")  # generator input
        gen_out = gen_model(input_gen)
        gen_with_disc = disc_model([input_gen, gen_out])
        g_train = Model(inputs=input_gen, outputs=[gen_with_disc, gen_out])
        opt_gen = Adam(lr=LEARNING_RATE_GEN, beta_1=0.5, name="opt_adv_adam")
        g_train.compile(
            optimizer=opt_gen,
            loss=["binary_crossentropy", "mae"],
            metrics=["accuracy"],
            loss_weights=[1, 100],
        )
        # --------------------------------------
        # define discriminator training model
        abstract = Input(shape=IMAGE_SIZE, name="Input_abstract_disc")
        real = Input(shape=IMAGE_SIZE, name="Input_real_disc")
        """This section is important. We create two input layers for the discriminator
        so that we can compare the abstract with the real and the generated image.
        Then we combine the inputs into one model so that they are trained together"""
        shared_1 = disc_model([abstract, real])
        shared_2 = disc_model([abstract, gen_model(abstract)])
        comb_disc = Concatenate()([shared_1, shared_2])
        d_train = Model(inputs=[abstract, real], outputs=comb_disc)
        opt_disc = Adam(lr=LEARNING_RATE_GEN, beta_1=0.5, name="opt_disc_adam")
        d_train.compile(
            optimizer=opt_disc, loss="binary_crossentropy", metrics=["accuracy"]
        )
        # --------------------------------------
        # training loop with checkpoints
        for j in range(0, checkpoint):
            print("\n\n######################################")
            print("Cycle ", i * checkpoint + j + 1, "/", cycles)
            print("######################################")
            # Get data
            abs_data, real_data = load_data()
            y_gen = create_y_values_gen(size_batch=size_batch)
            y_disc = create_y_values_disc()
            # --------------------------------------
            # Train Discriminator
            gen_model.trainable = False
            disc_model.trainable = True
            d_train.compile(
                optimizer=opt_disc, loss="binary_crossentropy", metrics=["accuracy"]
            )  # Recompile to set trainable
            history_disc = d_train.fit(
                x=[abs_data, real_data], y=y_disc, batch_size=1, epochs=1
            )
            try:
                key = "acc"
                last = len(history_disc.history[key])
            except KeyError:
                key = "accuracy"
                last = len(history_disc.history[key])
            if history_disc.history[key][last - 1] < 0.8:
                history_disc = d_train.fit(
                    x=[abs_data, real_data], y=y_disc, batch_size=1, epochs=1
                )
            # --------------------------------------
            # Train Generator
            gen_model.trainable = True
            disc_model.trainable = False
            g_train.compile(
                optimizer=opt_gen,
                loss=["binary_crossentropy", "mae"],
                metrics=["accuracy"],
                loss_weights=[1, 100],
            )  # Recompile to set trainable
            history_gen = g_train.fit(
                x=[abs_data], y=[y_gen, np.asarray(real_data)], batch_size=1, epochs=1
            )
            last = len(
                history_gen.history["Discriminator_" + key]
            )  # Here 'Discriminator' refers to adversarial loss
            while history_gen.history["Discriminator_" + key][last - 1] < 0.8:
                history_gen = g_train.fit(
                    x=[abs_data], y=[y_gen, np.asarray(real_data)], batch_size=1, epochs=1
                )
        # -------------------------------------------------------------------------------
        # save a checkpoint and clear the session to manage memory leaks from recompiling
        print("\nSaving checkpoint...")
        gen_model.trainable = True
        disc_model.trainable = True
        checkpoint_disc(model=disc_model, history=history_disc)
        checkpoint_gen(model=gen_model, history=history_gen)
        checkpoint_image(gen_model=gen_model)
        backend.clear_session()
        cpu_config()
        disc_model, gen_model = load_disc_gen()
        


###########################################################
# Main
###########################################################
def main():
    train(
        model=arguments.model,
        size_batch=arguments.size_batch,
        cycles=arguments.cycles,
        checkpoint=arguments.check_freq,
    )


if __name__ == "__main__":
    main()
