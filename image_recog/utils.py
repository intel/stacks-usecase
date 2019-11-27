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
"""utils to download and preprocess the model and img files"""
import errno
import os

import logging
from efficientnet_pytorch import EfficientNet
from PIL import Image
import torch
from torchvision import transforms
import traceback


logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def get_model(model_name="efficientnet-b0"):
    if not os.path.exists("./models/{}".format(model_name)):
        model = EfficientNet.from_pretrained(model_name)
        save_model_files(model, path="./models/", file_name=model_name)
    else:
        model = EfficientNet.from_name(model_name)
        model.load_state_dict(torch.load("./models/{}".format(model_name)))
    logger.debug("using model:{} ".format(model_name))
    return model


def _mkdir(path):
    """create directories recursively."""
    try:
        os.makedirs(path)
    except OSError as e:
        logger.debug("path {} already exists".format(path))
        if e.errno != errno.EEXIST:
            raise


def save_model_files(model, path, file_name):
    """save model data to path, create path if not exists"""
    try:
        _mkdir(path)
        torch.save(model.state_dict(), os.path.join(path, file_name))
    except Exception:
        logger.error(traceback.format_exc())


def preprocess_img(img):
    try:
        img = Image.open(img)
    except AttributeError:
        pass
    transform = transforms.Compose(
        [
            transforms.Resize(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    return transform(img).unsqueeze(0)
