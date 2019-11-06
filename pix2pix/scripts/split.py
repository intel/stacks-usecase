# Split the raw data into two images

import math
from glob import glob

from PIL import Image

from helper import get_directory


def split_images():
    """Load images from disk, split them, and save them to disk"""
    home_dir = get_directory()

    count = 0
    for f_name in glob(home_dir + "/data/raw/facades/**/*.jpg", recursive=True):

        # load image and find bounds
        tmp_img = Image.open(f_name)
        width, height = tmp_img.size
        middle = int(math.ceil(width / 2))

        # crop real image and input image
        real_box = (0, 0, middle, height)
        real_img = tmp_img.crop(real_box)
        input_box = (middle, 0, width, height)
        input_img = tmp_img.crop(input_box)

        # save images
        real_img.save(home_dir + "/data/tidy/real/" + str(count) + ".jpg")
        input_img.save(home_dir + "/data/tidy/input/" + str(count) + ".jpg")

        count += 1

    return True


if __name__ == "__main__":
    split_images()
