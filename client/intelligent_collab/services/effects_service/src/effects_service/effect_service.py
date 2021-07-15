import threading
import traceback
import sys
from typing import Dict

import numpy as np
import zmq

import config
from effect_server import EffectServer
from exceptions import EffectApplyException
from effect_picker import get_current_effect, unset_effect
from logger import logger
from similarity import Similarity as similar


eserver = EffectServer(port=config.ZMQ_PORT)

# hacky,could be improved by adding n previous frames and compare
CACHED_IMG: Dict[str, np.ndarray] = {
    "in_img": np.ndarray([0]),
    "e_img": np.ndarray([0]),
}


def _apply(effect, image_data: np.ndarray) -> np.ndarray:
    """if input frame is similar to previous frame, return cached effect,
    otherwise apply effect."""
    if config.app.state.config.get("cache", 0):
        global CACHED_IMG
        if (
            CACHED_IMG["e_img"].any()
            and similar(image_data, CACHED_IMG["in_img"]).mae()
        ):
            image_data = CACHED_IMG["e_img"]
        else:
            try:
                CACHED_IMG["in_img"] = image_data
                image_data = effect.apply(image_data)
                CACHED_IMG["e_img"] = image_data
            except Exception as ex:
                CACHED_IMG["i_img"] = np.ndarray([0])
                CACHED_IMG["e_img"] = np.ndarray([0])
                raise EffectApplyException from ex
    else:
        try:
            image_data = effect.apply(image_data)
        except Exception as ex:
            raise EffectApplyException from ex
    return image_data


def run(eserver: EffectServer):
    """apply effect to recieved frames and send modified frames to the client."""
    try:
        while eserver.on:
            try:
                image_data = eserver.recv()
                effect = get_current_effect()
                if effect:
                    try:
                        image_data = _apply(effect, image_data)
                    except EffectApplyException as e:
                        logger.error(
                            f"Effect {effect} cannot be applied, exception raise {e}"
                        )
                        logger.error(traceback.format_exc())
                        unset_effect()
                eserver.send(image_data)
            except zmq.error.ZMQError:
                logger.debug("Image recieved cannot be processed, skipping frame")
    except zmq.error.ContextTerminated:
        logger.debug("Effects server socket closed")
        sys.exit(0)


def start() -> dict:
    global eserver
    logger.debug("Starting effects service")
    on = eserver.on
    if on:
        logger.debug("Effects service already started")
    else:
        eserver.start()
        t = threading.Thread(
            target=run,
            args=(eserver,),
        )
        t.start()
        logger.debug("Effects service started")
    return get_status()


def stop() -> dict:
    global eserver
    logger.debug("Stopping effects service")
    on = eserver.on
    if on:
        eserver.close()
        logger.debug("Effects service stopped")
    else:
        logger.debug("Effects service not running")
    return get_status()


def get_status() -> dict:
    global eserver
    status = {"service": "off"}
    on = eserver.on
    if on:
        status["service"] = "on"
        status["port"] = config.ZMQ_PORT
    return status


if __name__ == "__main__":
    run(eserver)
