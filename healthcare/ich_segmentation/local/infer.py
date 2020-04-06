"""
Run local inference on ICH segmentation data
"""

import os

import tensorflow as tf
import numpy as np
from PIL import Image

from utils import helper
from local import physionet_preprocess as prep


def _save_images(predictions):
    img_name = 0
    home_dir = helper.get_directory()
    for x in predictions:
        img = np.uint8(np.reshape(x, (512, 512)) * 255)
        img = Image.fromarray(img, "L")
        filepath = os.path.join(
            home_dir, "local/inf_images/output", str(img_name) + ".png"
        )
        img.save(filepath, "PNG")
        img_name += 1


def _print_type_shape_max_min(x, name="x"):
    """ For debugging """
    print("\n", str(name), " type: ", type(x))
    print(str(name), " shape: ", x.shape)
    print(str(name), " max: ", np.amax(x))
    print(str(name), " min: ", np.amin(x))


def main():

    # run preprocess and save input and label pngs
    data_preprocess = prep.ICHDataPreprocess()
    dataset, labels = data_preprocess.preprocess()

    # call a TF.data.Data generator using the prepd data
    data_gen = prep.ICHDataGenerator(dataset, labels)
    train_img_label, test_img_label, train_len, test_len = data_gen.test_train_data()

    BATCH_SIZE = 32
    test_dataset = test_img_label.batch(BATCH_SIZE)

    # load model
    model = helper.load_unet()

    try:
        predictions = model.predict(test_dataset, steps=2)
    except:
        return 1  # prediction failed
    else:
        return 0  # prediction succeeded


if __name__ == "__main__":
    main()
