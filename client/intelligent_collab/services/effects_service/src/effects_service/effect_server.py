import time

import msgpack
import msgpack_numpy as mn
import numpy as np
import zmq

from logger import logger

mn.patch()


class EffectServer:
    def __init__(self, ip="*", port="5557"):
        self.url = f"tcp://{ip}:{port}"
        self.on = False

    def start(self):
        if not self.on:
            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.REP)
            logger.debug(f"Effects server bound to {self.url}")
            self.socket.bind(self.url)
            self.on = True

    def send(self, img_array: np.ndarray):
        """send msg using client."""
        packed_image = msgpack.packb(img_array, default=mn.encode)
        self.socket.send(packed_image)

    def recv(self):
        packed_effect_image = self.socket.recv()
        img_array = msgpack.unpackb(packed_effect_image, object_hook=mn.decode)
        return img_array

    def close(self):
        if self.on:
            self.on = False
            time.sleep(1)
            self.socket.close()
