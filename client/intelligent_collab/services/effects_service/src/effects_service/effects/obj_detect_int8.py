import os
import time


import numpy as np
import tensorflow as tf
import requests
from io import BytesIO
from PIL import Image

from object_detection.utils import label_map_util
from object_detection.utils import ops as utils_ops
from object_detection.utils import visualization_utils as viz_utils

from effects.base_effect import Effect
from effects.base_effect import npc
from logger import logger

EFFECT_MODEL = {
    "obj_detection_int8": {
        "path": "./models/ssd_mobilenet_int8",
        "img": {"crop": (300, 300)},
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


def parse_and_preprocess(serialized_example):
    # Dense features in Example proto.
    feature_map = {
        "image/encoded": tf.compat.v1.FixedLenFeature(
            [], dtype=tf.string, default_value=""
        ),
        "image/object/class/text": tf.compat.v1.VarLenFeature(dtype=tf.string),
        "image/source_id": tf.compat.v1.FixedLenFeature(
            [], dtype=tf.string, default_value=""
        ),
    }
    sparse_float32 = tf.compat.v1.VarLenFeature(dtype=tf.float32)
    # Sparse features in Example proto.
    feature_map.update(
        {
            k: sparse_float32
            for k in [
                "image/object/bbox/xmin",
                "image/object/bbox/ymin",
                "image/object/bbox/xmax",
                "image/object/bbox/ymax",
            ]
        }
    )
    features = tf.compat.v1.parse_single_example(serialized_example, feature_map)
    xmin = tf.expand_dims(features["image/object/bbox/xmin"].values, 0)
    ymin = tf.expand_dims(features["image/object/bbox/ymin"].values, 0)
    xmax = tf.expand_dims(features["image/object/bbox/xmax"].values, 0)
    ymax = tf.expand_dims(features["image/object/bbox/ymax"].values, 0)
    # Note that we impose an ordering of (y, x) just to make life difficult.
    bbox = tf.concat([ymin, xmin, ymax, xmax], 0)
    # Force the variable number of bounding boxes into the shape
    # [1, num_boxes, coords].
    bbox = tf.expand_dims(bbox, 0)
    bbox = tf.transpose(bbox, [0, 2, 1])
    encoded_image = features["image/encoded"]
    image_tensor = tf.image.decode_image(encoded_image, channels=3)
    image_tensor.set_shape([None, None, 3])
    label = features["image/object/class/text"].values
    image_id = features["image/source_id"]
    return image_tensor, bbox[0], label, image_id


class ObjectDetectionInt8(Effect):
    def __init__(self):
        self.model = EFFECT_MODEL.get("obj_detection_int8")
        self.config = tf.compat.v1.ConfigProto()
        self.config.intra_op_parallelism_threads = int(npc())
        self.config.inter_op_parallelism_threads = 1
        self.config.use_per_session_threads = 1
        self.batch_size = 1

    def _preprocess_image(self, img_array):
        """expand dims if required."""
        if len(img_array.shape) == 3:
            return np.expand_dims(img_array, 0)
        else:
            return img_array

    def _preprocess_graph(self):
        preprocess_graph = tf.Graph()

        with preprocess_graph.as_default():
            graph_def = tf.compat.v1.GraphDef()
            with tf.io.gfile.GFile(
                os.path.join(self.model["path"], "ssdmobilenet_preprocess.pb"), "rb"
            ) as input_file:
                input_graph_content = input_file.read()
                graph_def.ParseFromString(input_graph_content)
            tf.import_graph_def(graph_def, name="")
        self.pre_sess = tf.compat.v1.Session(graph=preprocess_graph, config=self.config)
        self.pre_output = preprocess_graph.get_tensor_by_name("Preprocessor/sub:0")
        self.pre_input = preprocess_graph.get_tensor_by_name("image_tensor:0")

    def load(self):
        l_time = time.time()
        self.infer_graph = tf.Graph()
        with tf.compat.v1.Session(graph=self.infer_graph, config=self.config):
            self._preprocess_graph()
        with self.infer_graph.as_default():
            graph_def = tf.compat.v1.GraphDef()
            with tf.io.gfile.GFile(
                os.path.join(
                    self.model["path"],
                    "ssdmobilenet_int8_pretrained_model_combinedNMS_s8.pb",
                ),
                "rb",
            ) as input_file:
                input_graph_content = input_file.read()
                graph_def.ParseFromString(input_graph_content)
            tf.import_graph_def(graph_def, name="")
        self.session = tf.compat.v1.Session(graph=self.infer_graph, config=self.config)
        input_layer = "Preprocessor/subpart2"
        output_layers = [
            "num_detections",
            "detection_boxes",
            "detection_scores",
            "detection_classes",
        ]
        self.input_tensor = self.infer_graph.get_tensor_by_name(input_layer + ":0")
        self.output_tensors = [
            self.infer_graph.get_tensor_by_name(x + ":0") for x in output_layers
        ]
        logger.debug("## >> load-time {:.2f} s".format(time.time() - l_time))

    def apply(self, img_array):
        self.input_image = self._preprocess_image(img_array)
        e_t = time.time()
        input_image = self.input_image
        i_t = time.time()
        input_image = self.pre_sess.run(self.pre_output, {self.pre_input: input_image})
        num, boxes, scores, labels = self.session.run(
            self.output_tensors, {self.input_tensor: input_image}
        )
        logger.debug("## >> i-time {:.2f} s".format(time.time() - i_t))
        self.detection = {}
        num = int(num[0])
        self.detection["boxes"] = np.asarray(boxes[0])[0:num]
        self.detection["scores"] = np.asarray(scores[0])[0:num]
        self.detection["classes"] = np.asarray(labels[0])[0:num]
        self.postprocess()
        logger.debug("## >> e-time {:.2f} s".format(time.time() - e_t))
        return self.modified_img_array

    def postprocess(self):
        """process input image with the effect

        params
        img_array: numpy array  of internal image
        effect: dictionary of effects from the model.
        """
        effects_img = self.input_image.copy()
        viz_utils.visualize_boxes_and_labels_on_image_array(
            effects_img[0],
            self.detection["boxes"],
            self.detection["classes"].astype(int),
            self.detection["scores"],
            CATEGORY_MAP,
            use_normalized_coordinates=True,
            max_boxes_to_draw=10,
            min_score_thresh=0.35,
            agnostic_mode=False,
            keypoint_edges=COCO17_HUMAN_POSE_KEYPOINTS,
        )
        self.modified_img_array = effects_img[0]
        # to debug effect, save image to local
        # save_image_array(self.modified_img_array, "bbox_int8")


if __name__ == "__main__":

    def get_image():
        image_url = (
            "https://upload.wikimedia.org/wikipedia/commons/6/60/Naxos_Taverna.jpg"
        )
        return get_image_array(image_url)

    def save_image_array(array, name):
        img = Image.fromarray(np.uint8(array)).convert("RGB")
        img.save(name + ".jpg")

    def get_image_array(path):
        """get image and return as numpy array."""
        image = None
        if path.startswith("http"):
            image_data = requests.get(path).content
            image_data = BytesIO(image_data)
            image = Image.open(image_data)
        else:
            image_data = tf.io.gfile.GFile(path, "rb").read()
            image = Image.open(BytesIO(image_data))
        (im_width, im_height) = image.size
        img_array = (
            np.array(image.getdata())
            .reshape((1, im_height, im_width, 3))
            .astype(np.float32)
        )
        return img_array

    effect = ObjectDetectionInt8()
    effect.load()
    img_array = get_image()
    i = 10
    while True:
        i = i - 1
        effect.apply(img_array)
        if i == 0:
            break
