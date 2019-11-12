###########################################################
# Pix2pix keras/tensorflow inference
###########################################################
import io
import logging
import os
import time
from binascii import b2a_base64

import fire  # noqa
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras import backend
from tensorflow.keras.models import load_model


from scripts.helper import get_directory, get_cpuinfo, norm_data, reverse_norm

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# debug - supressing tensorflow warnings
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
os.environ["PYTHONWARNINGS"] = "ignore"

# intel optimizations
num_cores, num_sockets = get_cpuinfo()
os.environ["KMP_AFFINITY"] = "granularity=fine,verbose,compact,1,0"
os.environ["KMP_BLOCKTIME"] = "1"
os.environ["OMP_NUM_THREADS"] = str(num_cores * 2)
backend.set_session(
    tf.Session(
        config=tf.ConfigProto(
            intra_op_parallelism_threads=num_cores * 2,
            inter_op_parallelism_threads=num_sockets,
        )
    )
)


def infer(img):
    """inference function, accepts an abstract image file return generated image"""
    home_dir = get_directory()
    # load model
    backend.clear_session()
    gen_model = load_model(home_dir + "/models/generator_model.h5", compile=False)
    img = np.array(Image.open(img))
    img = norm_data([img])
    s_time = time.time()
    result = gen_model.predict(img[0].reshape(1, 256, 256, 3))
    f_time = time.time()
    logger.info(
        "\033[92m"
        + "[INFO] "
        + "\033[0m"
        + "Inference done in: {:2.3f} seconds".format(f_time - s_time)
    )
    # transform result from normalized to absolute values and convert to image object
    result = Image.fromarray(reverse_norm(result[0]), "RGB")
    # for debugging, uncomment the line below to inspect the generated image locally
    # result.save("generted_img.jpg", "JPEG")
    # convert image to bytes object to send it to the client
    binary_buffer = io.BytesIO()
    result.save(binary_buffer, format="JPEG")
    return b2a_base64(binary_buffer.getvalue())


if __name__ == "__main__":
    logger.info("\033[92m" + "[INFO] " + "\033[0m" + " : initializing inference..")
    # to debug locally, uncomment the line below and run python infer.py image.jpg
    fire.Fire(infer)
