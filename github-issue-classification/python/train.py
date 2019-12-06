#!usr/bin/env python
#
# Copyright (c) 2019 Intel Corporation
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from glob import glob
import logging
import sys
import pickle
import os

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import GRU
from tensorflow.keras import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BATCH_SIZE = 128
EPOCH = 30
N_NODES = 1000

try:
    DATADIR = os.getenv("DATASET_PATH") + "/tidy/"
except KeyError:
    DATADIR = "/workdir/data/tidy/"


def _fcn(dim=1000, classes=10, dropout=0.3):
    "fully connected net."
    _model = Sequential()
    _model.add(Dense(dim, input_dim=dim, activation="relu"))
    _model.add(Dropout(dropout))
    _model.add(Dense(dim * 0.7, activation="relu"))
    _model.add(Dropout(dropout))
    _model.add(Dense(dim * 0.7, activation="relu"))
    _model.add(Dropout(dropout))
    _model.add(Dense(dim * 0.5, activation="relu"))
    _model.add(Dropout(dropout))
    _model.add(Dense(10, activation="sigmoid"))
    return _model


def _rnn(dim=1000, classes=10, dropout=0.6):
    """recurrent model"""
    _model = Sequential()
    _model.add(Embedding(dim, 64))
    _model.add(GRU(64))
    _model.add(Dense(64, activation="relu"))
    _model.add(Dropout(dropout))
    _model.add(Dense(10, activation="sigmoid"))
    return _model


def _save_data(data, file_name=None):
    with open(file_name, "wb") as f_handle:
        pickle.dump(data, f_handle)


def model_def(fcn=True, dim=1000):
    """model compiler"""
    if fcn:
        model = _fcn(dim=1000, classes=10)
    else:
        model = _rnn(dim=1000, classes=10)
    model.compile(loss="binary_crossentropy",
                  optimizer="adam", metrics=["accuracy"])
    return model


def plot_metrics(history, metric):
    """plot train and test metrics."""
    plt.plot(history.history(metric))
    plt.plot(history.history["val_" + metric], "")
    plt.xlabel("Epochs")
    plt.y_label(metric)
    plt.legend([metric, "val_" + metric])
    plt.show()


def dataset(test_size=0.33, random_state=42):
    """split body and label to train and test batches"""
    df = pd.DataFrame()
    # Read data from disk
    workdir = DATADIR + "*.json"

    # for f_name in glob("/workdir/data/tidy/*.json"):
    for f_name in glob(workdir):
        df_temp = pd.read_json(f_name, lines=True)
        df = df.append(df_temp)
    return train_test_split(df["body"], df["labels"], test_size=test_size, random_state=random_state)


def feature_vectorizer(X_train, X_test, y_train, y_test):
    """prepare X data with tfidf and y with multi label binarizer"""
    vectorizer = TfidfVectorizer(
        analyzer="word", min_df=0.0,
        max_df=1.0, strip_accents=None,
        encoding="utf-8", preprocessor=None,
        token_pattern=r"(?u)\S\S+", max_features=1000,
    )
    # fit only training data
    vectorizer.fit(X_train)
    _save_data(vectorizer, "/workdir/models/X_vectorizer.pk")
    X_train_features = vectorizer.transform(X_train)
    X_test_features = vectorizer.transform(X_test)
    # use multiLabelBinarizer to create one-hot encoding of labels for y data
    mlb = MultiLabelBinarizer()
    # fit only training data
    mlb.fit(y_train)
    _save_data(mlb, "/workdir/models/label_binarizer.pk")
    y_train_features = mlb.transform(y_train)
    y_test_features = mlb.transform(y_test)
    return X_train_features, X_test_features, y_train_features, y_test_features


def train(plot=False):
    X_train, X_test, y_train, y_test = feature_vectorizer(*dataset())
    # define and train Model
    model = model_def(N_NODES)
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test), epochs=EPOCH,
        batch_size=BATCH_SIZE, verbose=1)
    model.save("/workdir/models/git-model.h5")
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    logger.debug("Test accuracy: {:2.2f}".format(test_accuracy * 100))
    logger.debug("Test loss: {:2.2f}".format(test_loss))
    if plot:
        plot_metrics(history, "loss")



if __name__ == "__main__":
    train()
