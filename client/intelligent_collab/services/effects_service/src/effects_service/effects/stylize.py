"""style a frame using magenta_image_style_v1-256_2 model from tf hub"""

import os
import time

import matplotlib.pyplot as plt
import numpy as np
import tensorflow_hub as thub
import tensorflow as tf

from effects.base_effect import Effect
from logger import logger

EFFECT_MODEL = {
    "stylize": {
        "path": "models/magenta_arbitrary-image-stylization-v1-256_2",
        "data": "data/lighouse.jpg",
    }
}


class Stylize(Effect):
    """apply stylized effect."""

    def __init__(self):
        self.model: dict = EFFECT_MODEL.get("stylize")
        self.style_golden = self.load_golden_image(self.model["data"])
        self.detector = None
        self.img_array = None
        self.modified_img_array = None

    @staticmethod
    def _crop_center(image):
        """Returns a cropped square image."""
        shape = image.shape
        new_shape = min(shape[1], shape[2])
        offset_y = max(shape[1] - shape[2], 0) // 2
        offset_x = max(shape[2] - shape[1], 0) // 2
        image = tf.image.crop_to_bounding_box(
            image, offset_y, offset_x, new_shape, new_shape
        )
        return image

    def load_golden_image(self, image_path, size=(256, 256)):
        img_array = plt.imread(image_path).astype(np.float32)[np.newaxis, ...]
        img_array = self.preprocess(img_array)
        img_array = tf.image.resize(img_array, size, preserve_aspect_ratio=True)
        img_array = self._crop_center(img_array)
        return img_array

    def load(self):
        """load model from path bound to local from the container."""
        l_time = time.time()
        self.detector = thub.load(self.model["path"])
        self.detector(tf.constant(self.style_golden), tf.constant(self.style_golden))
        logger.debug("#>> load-tme {:.3f}".format(time.time() - l_time))

    @staticmethod
    def preprocess(img_array):
        """preprocess the input image."""
        if img_array.dtype != np.float32:
            img_array = img_array.astype(np.float32)
        if img_array.max() > 1.0:
            img_array = img_array / 255.0
        if len(img_array.shape) == 3:
            img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.image.resize(
            img_array,
            (img_array.shape[1], img_array.shape[2]),
            preserve_aspect_ratio=True,
        )
        return img_array

    def apply(self, img_array):
        """apply effect to an image array.
        preprocess the image
        call the detector, pass the image,
        postprocess image, add effects.
        """
        e_time = time.time()
        self.img_array = self.preprocess(img_array)
        self.style_golden = tf.nn.avg_pool(
            self.style_golden, ksize=[3, 3], strides=[1, 1], padding="SAME"
        )
        i_time = time.perf_counter()
        self.effect = self.detector(self.img_array, self.style_golden)
        logger.debug("#>> i-time {:.3f}".format(time.perf_counter() - i_time))
        self.postprocess()
        logger.debug("#>> e-time {:.3f}".format(time.time() - e_time))
        return self.modified_img_array[0]

    def postprocess(self):
        """process input image with the effect

        params
        img_array: numpy array  of internal image
        effect: dictionary of effects from the model.
        """
        mod_array = self.effect[0].numpy()
        self.modified_img_array = np.rint(np.interp(mod_array, (0, 1), (0, 255))).astype(dtype="uint8")
