import os
import time

import numpy as np
import tensorflow_hub as thub
import tensorflow as tf

from object_detection.utils import label_map_util
from object_detection.utils import ops as utils_ops
from object_detection.utils import visualization_utils as viz_utils

from effects.base_effect import Effect
from logger import logger

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

EFFECT_MODEL = {
    "obj_detection": {
        "path": "models/ssd_mobilenet_v2_2",
        "img": {"crop": (1280, 856)},
    }
}


COCO17_HUMAN_POSE_KEYPOINTS = [
    (0, 1),
    (0, 2),
    (1, 3),
    (2, 4),
    (0, 5),
    (0, 6),
    (5, 7),
    (7, 9),
    (6, 8),
    (8, 10),
    (5, 6),
    (5, 11),
    (6, 12),
    (11, 12),
    (11, 13),
    (13, 15),
    (12, 14),
    (14, 16),
]

CATEGORY_MAP = {
    1: {"id": 1, "name": "person"},
    2: {"id": 2, "name": "bicycle"},
    3: {"id": 3, "name": "car"},
    4: {"id": 4, "name": "motorcycle"},
    5: {"id": 5, "name": "airplane"},
    6: {"id": 6, "name": "bus"},
    7: {"id": 7, "name": "train"},
    8: {"id": 8, "name": "truck"},
    9: {"id": 9, "name": "boat"},
    10: {"id": 10, "name": "traffic light"},
    11: {"id": 11, "name": "fire hydrant"},
    13: {"id": 13, "name": "stop sign"},
    14: {"id": 14, "name": "parking meter"},
    15: {"id": 15, "name": "bench"},
    16: {"id": 16, "name": "bird"},
    17: {"id": 17, "name": "cat"},
    18: {"id": 18, "name": "dog"},
    19: {"id": 19, "name": "horse"},
    20: {"id": 20, "name": "sheep"},
    21: {"id": 21, "name": "cow"},
    22: {"id": 22, "name": "elephant"},
    23: {"id": 23, "name": "bear"},
    24: {"id": 24, "name": "zebra"},
    25: {"id": 25, "name": "giraffe"},
    27: {"id": 27, "name": "backpack"},
    28: {"id": 28, "name": "umbrella"},
    31: {"id": 31, "name": "handbag"},
    32: {"id": 32, "name": "tie"},
    33: {"id": 33, "name": "suitcase"},
    34: {"id": 34, "name": "frisbee"},
    35: {"id": 35, "name": "skis"},
    36: {"id": 36, "name": "snowboard"},
    37: {"id": 37, "name": "sports ball"},
    38: {"id": 38, "name": "kite"},
    39: {"id": 39, "name": "baseball bat"},
    40: {"id": 40, "name": "baseball glove"},
    41: {"id": 41, "name": "skateboard"},
    42: {"id": 42, "name": "surfboard"},
    43: {"id": 43, "name": "tennis racket"},
    44: {"id": 44, "name": "bottle"},
    46: {"id": 46, "name": "wine glass"},
    47: {"id": 47, "name": "cup"},
    48: {"id": 48, "name": "fork"},
    49: {"id": 49, "name": "knife"},
    50: {"id": 50, "name": "spoon"},
    51: {"id": 51, "name": "bowl"},
    52: {"id": 52, "name": "banana"},
    53: {"id": 53, "name": "apple"},
    54: {"id": 54, "name": "sandwich"},
    55: {"id": 55, "name": "orange"},
    56: {"id": 56, "name": "broccoli"},
    57: {"id": 57, "name": "carrot"},
    58: {"id": 58, "name": "hot dog"},
    59: {"id": 59, "name": "pizza"},
    60: {"id": 60, "name": "donut"},
    61: {"id": 61, "name": "cake"},
    62: {"id": 62, "name": "chair"},
    63: {"id": 63, "name": "couch"},
    64: {"id": 64, "name": "potted plant"},
    65: {"id": 65, "name": "bed"},
    67: {"id": 67, "name": "dining table"},
    70: {"id": 70, "name": "toilet"},
    72: {"id": 72, "name": "tv"},
    73: {"id": 73, "name": "laptop"},
    74: {"id": 74, "name": "mouse"},
    75: {"id": 75, "name": "remote"},
    76: {"id": 76, "name": "keyboard"},
    77: {"id": 77, "name": "cell phone"},
    78: {"id": 78, "name": "microwave"},
    79: {"id": 79, "name": "oven"},
    80: {"id": 80, "name": "toaster"},
    81: {"id": 81, "name": "sink"},
    82: {"id": 82, "name": "refrigerator"},
    84: {"id": 84, "name": "book"},
    85: {"id": 85, "name": "clock"},
    86: {"id": 86, "name": "vase"},
    87: {"id": 87, "name": "scissors"},
    88: {"id": 88, "name": "teddy bear"},
    89: {"id": 89, "name": "hair drier"},
    90: {"id": 90, "name": "toothbrush"},
}


class ObjectDetection(Effect):
    """apply object detection effect."""

    def __init__(self):
        self.model: dict = EFFECT_MODEL.get("obj_detection")
        self.detector = None
        self.img_array = None
        self.modified_img_array = None

    def load(self):
        """load model from path bound to local from the container."""
        l_time = time.time()
        self.detector = thub.load(self.model["path"])
        self.detector(np.random.random((1, 256, 256, 3)))
        logger.debug("## >> load-time {:.2f} s".format(time.time() - l_time))

    def preprocess(self, img_array):
        """preprocess the input image."""
        if len(img_array.shape) == 3:
            self.img_array = np.expand_dims(img_array, 0)
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
        i_time = time.perf_counter()
        effect: dict = self.detector(self.img_array)
        logger.debug("## >> i-time {:.2f} s".format(time.perf_counter() - i_time))
        self.effect: dict = {key: value.numpy() for key, value in effect.items()}
        self.postprocess()
        logger.debug("## >> e-time {:.2f} s".format(time.time() - e_time))
        return self.modified_img_array

    def postprocess(self):
        """process input image with the effect

        params
        img_array: numpy array  of internal image
        effect: dictionary of effects from the model.
        """
        effect = self.effect
        effects_img = self.img_array.copy()
        keypoints = effect.get("detection_keypoints")
        keypoint_scores = effect.get("detection_keypoint_scores")
        if keypoints:
            keypoint_scores = effect.get("detection_keypoint_scores")[0]
        viz_utils.visualize_boxes_and_labels_on_image_array(
            effects_img[0],
            effect["detection_boxes"][0],
            effect["detection_classes"][0].astype(int),
            effect["detection_scores"][0],
            CATEGORY_MAP,
            use_normalized_coordinates=True,
            max_boxes_to_draw=10,
            min_score_thresh=0.60,
            agnostic_mode=False,
            keypoints=keypoints,
            keypoint_scores=keypoint_scores,
            keypoint_edges=COCO17_HUMAN_POSE_KEYPOINTS,
        )
        self.modified_img_array = effects_img[0]
