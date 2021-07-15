import os
import time

import numpy as np

from effects.base_effect import Effect
from logger import logger


class Flip(Effect):
    """flip image"""

    def __init__(self):
        self.detector = None
        self.img_array = None
        self.modified_img_array = None

    @staticmethod
    def load():
        """load model from path bound to local from the container."""
        l_time = time.time()
        logger.debug("## >> load-time {:.2f} s".format(time.time() - l_time))

    def preprocess(self, img_array):
        """preprocess the input image."""
        if img_array.shape == 4:
            self.img_array = img_array[0]
        else:
            self.img_array = img_array

    def apply(self, img_array):
        """apply effect to an image array.
        preprocess the image
        call the detector, pass the image,
        postprocess image, add effects.
        """
        e_time = time.time()
        self.preprocess(img_array)
        self.modified_img_array = np.fliplr(self.img_array)
        i_time = time.perf_counter()
        logger.debug("## >> i-time {:.2f} s".format(time.perf_counter() - i_time))
        self.postprocess()
        logger.debug("## >> e-time {:.2f} s".format(time.time() - e_time))
        return self.modified_img_array

    @staticmethod
    def postprocess():
        """process input image with the effect

        params
        img_array: numpy array  of internal image
        effect: dictionary of effects from the model.
        """
        pass
