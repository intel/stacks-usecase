import sys

from logger import logger

import config

def get_stream_direction():
    source = get_current_source()
    if source is None:
        return None
    if source["source"].isdigit():
        return "outgoing"
    return "incoming"


def set_source(source: dict):
    logger.debug("Setting new video source")
    current_source = config.app.state.config.get("video_source", None)
    if source != current_source:
        # If new values are null, keep old config
        if current_source is not None:
            for k, v in current_source.items():
                new_v = source.get(k, v)
                current_source[k] = new_v if new_v is not None else v
        else:
            current_source = source
        config.app.state.config["video_source"] = current_source
        return current_source
    else:
        logger.debug(f"Source {source['source']} already current")
    return current_source


def unset_source():
    config.app.state.config["video_source"] = None


def get_current_source():
    current_source = config.app.state.config.get("video_source", None)
    return current_source


def set_virtual_device(virtual_device: int):
    logger.debug("Setting current virtual_device")
    current_device = config.app.state.config.get("virtual_device", None)
    if virtual_device != current_device:
        config.app.state.config["virtual_device"] = virtual_device
        return virtual_device
    else:
        logger.debug(f"Virtual Device {virtual_device} already current")
    return current_device


def unset_virtual_device():
    config.app.state.config["virtual_device"] = None


def get_current_virtual_device():
    current_device = config.app.state.config.get("virtual_device", None)
    return current_device
