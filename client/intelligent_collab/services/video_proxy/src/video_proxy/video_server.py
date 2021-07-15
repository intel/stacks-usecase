import time
import os

import msgpack
import msgpack_numpy as mn
import numpy as np
import zmq
import cv2
import pyfakewebcam

from logger import logger
from video_settings import get_current_source
from video_settings import get_current_virtual_device
from video_settings import get_stream_direction

mn.patch()

class VideoServer:
    def __init__(self, ip="127.0.0.1", port="5555"):
        self.url = f"tcp://{ip}:{port}"
        self.on = False
        self.vcam_id = None
        self.w = None
        self.h = None
        self.vcam = None
        self.source = None
        self.capture = None
        self.vcam_used = False

    def start(self):
        if not self.on:
            self.set_source_object()
            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.REQ)
            logger.debug(f"Video socket connecting to {self.url}")
            self.socket.connect(self.url)
            self.on = True

    def set_source_object(self):
        if get_current_source() != self.source:
            self.source = get_current_source().copy()
            if get_stream_direction() == "incoming":
                #TODO generate object for capturing from URL
                #self.capture = URLframeCapture(get_current_source())
                pass
            else:
                if self.capture:
                    logger.debug("Closing previous capture instance")
                    self.capture.release()
                logger.debug(f"Instancing a new capture device {self.source}")
                self.capture = cv2.VideoCapture(int(self.source["source"]))
                if self.source.get("pix_fmt"):
                    fourcc = list(self.source["pix_fmt"].ljust(4))
                    self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*fourcc))
                if self.source.get("res"):
                    width, height = self.source["res"].split("x")
                    self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, int(width))
                    self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, int(height))
                logger.debug(f"Capture device open {self.capture.isOpened()}")
            logger.debug(f"Changing video source to {self.source}")

    def is_ready(self):
        if get_current_source() is None:
            logger.debug("Video source has not been set")
            return False
        if get_current_virtual_device() is None:
            logger.debug("ICcam ID has not been set")
            return False
        return True

    def get_frame(self):
        #TODO: avoid evaluluate stream direction if capture object implements a read() method returning a tuple
        _, image = self.capture.read()
        return image

    def sink(self, frame):
        w = frame.shape[1]
        h = frame.shape[0]
        vcam_id = get_current_virtual_device()
        if w != self.w or h != self.h or vcam_id != self.vcam_id:
            self.vcam_id = vcam_id
            if self.vcam:
                os.close(self.vcam._video_device)
            self.vcam = pyfakewebcam.FakeWebcam(f"/dev/video{self.vcam_id}", w, h)
            if self.vcam._settings.fmt.pix.width == w and self.vcam._settings.fmt.pix.height == h:
                self.w = w
                self.h = h
                self.vcam_used = False
            else:
                if not self.vcam_used:
                    logger.warning(f"Sink device is being used and is preventing to change resolution, please close any other apps using /dev/video{self.vcam_id}")
                    self.vcam_used = True
                return
            logger.debug("Output parameters have changed")
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.vcam.schedule_frame(frame_rgb)

    def send(self, img_array: np.ndarray):
        packed_image = msgpack.packb(img_array, default=mn.encode)
        self.socket.send(packed_image)

    def recv(self):
        packed_effect_image = self.socket.recv()
        img_array = msgpack.unpackb(packed_effect_image, object_hook=mn.decode)
        return img_array

    def close(self):
        if self.on:
            self.on = False
            self.vcam_id = None
            self.w = None
            self.h = None
            self.source = None
            if self.vcam:
                os.close(self.vcam._video_device)
                self.vcam = None
            #TODO: avoid evaluluate stream direction if capture object implements a release() method
            if self.capture:
                self.capture.release()
                self.capture = None
            time.sleep(1)
            self.socket.close()
