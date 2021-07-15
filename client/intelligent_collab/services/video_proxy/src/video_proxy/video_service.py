import threading
import sys

import zmq

from video_server import VideoServer
from video_settings import get_stream_direction

from logger import logger
import config

vserver = VideoServer(ip=config.ZMQ_IP, port=config.ZMQ_PORT)

def run(vserver: VideoServer):
    try:
        while vserver.on:
            try:
                vserver.set_source_object()
                # logger.debug("Image read")
                image_data = vserver.get_frame()
                # logger.debug(f"Image read: {type(image_data)}")
                if image_data is not None:
                    # logger.debug("Image send")
                    vserver.send(image_data)
                    # logger.debug("Image recive")
                    image_data = vserver.recv()
                    # logger.debug(f"Image recived: {image_data}")
                    # logger.debug("Image sink")
                    vserver.sink(image_data)
                    # logger.debug("Done, continue")
            except zmq.error.ZMQError:
                logger.debug("Image recieved cannot be processed, skipping frame")
    except zmq.error.ContextTerminated:
        logger.debug("Video Proxy server socket closed")
        sys.exit(0)

def start() -> dict:
    global vserver
    logger.debug("Starting video proxy service")
    on = vserver.on
    if on:
        logger.debug("Video Proxy service already started")
    elif not vserver.is_ready():
        logger.debug("Video Proxy has not been configured yet")
    else:
        vserver.start()
        t = threading.Thread(target=run, args=(vserver,))
        t.start()
        logger.debug("Video Proxy service started")
    return get_status()


def stop() -> dict:
    global vserver
    logger.debug("Stopping video proxy service")
    on = vserver.on
    if on:
        vserver.close()
        logger.debug("Video Proxy service stopped")
    else:
        logger.debug("Video Proxy service not running")
    return get_status()


def get_status() -> dict:
    global vserver
    status = {
        'service': 'off'
    }
    on = vserver.on
    if on:
        status['service'] = 'on'
        status['port'] = config.ZMQ_PORT
    return status


if __name__ == "__main__":
    run(vserver)
