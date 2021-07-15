import os
import tensorflow as tf

from effects.utils import num_physical_cores as npc

# default flags
os.environ["OMP_NUM_THREADS"] = npc()
os.environ["KMP_SETTINGS"] = "TRUE"
os.environ["KMP_BLOCKTIME"] = "0"
os.environ["KMP_AFFINITY"] = "granularity=fine,compact,1,0"
# os.environ["TF_XLA_FLAGS"] = "--tf_xla_auto_jit=2 --tf_xla_cpu_global_jit"
tf.config.set_soft_device_placement(True)
tf.config.threading.set_inter_op_parallelism_threads(1)
tf.config.threading.set_intra_op_parallelism_threads(int(npc()))


class Effect:
    """Effects parent.

    load models and apply effects.

    """

    def __init__(self, name: str = ""):
        self.model: dict = {}
        self.detector = None
        self.img_array = None
        self.modified_img_array = None

    def load(self):
        """load model from path bound to local from the container."""
        pass

    def preprocess(self, img_array):
        """preprocess the input image."""
        self.img_array = img_array

    def apply(self, img_array):
        """apply effect to an image array.
        preprocess the image
        call the detector, pass the image,
        postprocess image, add effects.
        """
        self.preprocess(img_array)
        effect: dict = self.detector(self.img_array)
        self.effect: dict = {key: value.numpy() for key, value in effect.items()}
        self.postprocess()
        return self.modified_img_array

    def postprocess(self):
        """process input image with the effect

        params
        img_array: numpy array  of internal image
        effect: dictionary of effects from the model.
        """
        self.modified_img_array = self.img_array
