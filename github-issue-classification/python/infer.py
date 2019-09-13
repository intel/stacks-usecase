#!/usr/bin/env python
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

import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BATCH_SIZE = 128
EPOCH = 30
N_NODES = 1000


def feature_vectorizer(body):
    """prepare body data with trained tfidf vectorizer"""
    with open("/workdir/models/X_vectorizer.pk", "rb") as pickled_file:
        vectorizer = pickle.load(pickled_file)
    features = vectorizer.transform(body)
    return features


def infer(body=None):
    X = feature_vectorizer(body)
    model = load_model("/workdir/models/git-model.h5")
    prediction = model.predict(X, verbose=0)
    with open("/workdir/models/label_binarizer.pk", "rb") as pickled_file:
        mlb = pickle.load(pickled_file)
    return mlb.inverse_transform(np.round(prediction))


if __name__ == "__main__":
    body = [
        "use experimental_jit_scope to enable XLA:CPU.  To confirm that XLA is active"]
    log.debug("Given body: {}".format(body))
    log.debug("Possible classes: {}".format(infer(body)))
