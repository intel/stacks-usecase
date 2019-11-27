#!usr/bin/env python
#
# Copyright (c) 2019 Intel Corporation
#
# Main author:
#   * unrahul <rahul.unnikrishnan.nair@intelcom>
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
#
from itertools import islice

try:
    import rapidjson as rjson
except:
    import json as rjson
import torch

from utils import preprocess_img
from utils import save_model_files
from utils import get_model


def load_labels(index):
    """index labels and return predicted output."""

    labels_map = rjson.load(open("./data/labels_map.txt"))
    labels = (labels_map[str(i)] for i in range(1000))
    return next(islice(labels, index, None))


def predict(model, img):
    """given a model and input image, predict what it is."""

    model.eval()
    with torch.no_grad():
        y_hat = model(img)
    index = torch.topk(y_hat, k=1)[1]
    prob = torch.softmax(y_hat, dim=1)[0, index].item()
    y_hat = load_labels(index[0])
    return y_hat, prob


def classify(image):
    model = get_model("efficientnet-b0")
    img = preprocess_img(image)
    return predict(model, img)


if __name__ == "__main__":
    # TODO (unrahul) add a flask api layer
    y_hat = classify(image="./data/cat.jpg")
    print("img recognition test, data: ./data/cat.jpg")
    print("img is of an {0}".format(*y_hat))
