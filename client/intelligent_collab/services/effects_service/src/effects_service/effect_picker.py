import threading
import traceback

from logger import logger
from effects.flip import Flip
from effects.obj_detect import ObjectDetection
from effects.obj_detect_int8 import ObjectDetectionInt8
from effects.stylize import Stylize
from effects.flip import Flip
import config

effect_map = {
        "fast_object_detection": ObjectDetectionInt8(),
        "object_detection": ObjectDetection(),
        "stylize": Stylize(),
        "flip" : Flip()
        }


effect_meta = {
        "fast_object_detection": {
            "desc": "TensorFlow SSD MobileNet int8 model Optimized for Intel Hardware",
            "link": "https://github.com/IntelAI/models"
            },
            "object_detection": {
                "desc": "TensorFlow SSD MobileNet fp32 model from TensorFlow Hub",
                "link": "https://www.tensorflow.org/hub/tutorials/object_detection"
                },
        "stylize": {
            "desc": "Arbitarary Image Style Transfer implemented in Magenta library from TensorFlow Hub",
            "link": "https://www.tensorflow.org/hub/tutorials/tf2_arbitrary_image_stylization",
        },
        "flip" : {
            "desc": "OpenCV image flip",
            "link": "https://github.com/opencv/opencv-python"
            },
        }



def load_model(effect_name):
    logger.debug(f"Loading model {effect_name}")
    try:
        effect_map[effect_name].load()
        config.app.state.config["effect"] = (effect_name, True)
        logger.debug(f"Model {effect_name} loaded")
    except Exception as e:
        logger.error(f"Model {effect_name} can't load")
        logger.error(traceback.format_exc())
        unset_effect()


def list_effects() -> list:
    logger.debug("Listing available effects")
    current_effect, loaded = config.app.state.config.get("effect", (None, False))
    effect_list = []
    for effect_name in effect_map.keys():
        enabled = True if effect_name == current_effect else False
        loading = True if enabled and not loaded else False
        effect_list.append({
            "name": effect_name,
            "enabled": enabled,
            "loading": loading,
            "meta": effect_meta[effect_name],
        })
    return effect_list


def set_cache(cache: int=0):
    """set global cache option."""
    config.app.state.config["cache"] = cache
    return cache


def get_cache():
    """get global cache option."""
    return config.app.state.config.get("cache", 0)


def set_effect(effect_name: str):
    logger.debug("Setting current effect")
    current_effect, loaded = config.app.state.config.get("effect", (None, False))
    if effect_name in effect_map:
        if effect_name != current_effect:
            config.app.state.config["effect"] = (effect_name, False)
            t = threading.Thread(target=load_model, args=(effect_name,))
            t.start()
            return effect_name
        else:
            logger.debug(f"Effect {effect_name} already current")
    else:
        logger.debug(f"Effect {effect_name} not available")
    return current_effect


def unset_effect():
    config.app.state.config["effect"] = (None, False)


def get_current_effect():
    # logger.debug("Getting instance of current effect")
    current_effect, loaded = config.app.state.config.get("effect", (None, False))
    if current_effect and loaded:
        return effect_map[current_effect]
    # else:
    #     if not current_effect:
    #         logger.debug("Current effect not set")
    #     elif not loaded:
    #         logger.debug(f"Model {current_effect} not loaded yet")
    return None
