from io import BytesIO

import matplotlib.pyplot as plt
import msgpack
import msgpack_numpy as mn
import numpy as np
import requests
import tensorflow as tf
import zmq
from PIL import Image

mn.patch()


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
    return (
        np.array(image.getdata()).reshape((1, im_height, im_width, 3)).astype(np.uint8)
    )


class EffectClient:
    def __init__(self, ip="0.0.0.0", port="5557"):

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        url = f"tcp://{ip}:{port}"
        print(f"client using url: {url}")
        self.socket.connect(url)

    def send(self, img_array: np.ndarray):
        """send msg using client."""
        packed_image = msgpack.packb(img_array, default=mn.encode)
        self.socket.send(packed_image)


    def recv(self):
        packed_effect_image = self.socket.recv()
        print("recieved")
        img_array = msgpack.unpackb(packed_effect_image, object_hook=mn.decode)
        plt.imsave("bbox_img.png", img_array)
        #plt.imsave("stylized_img.png", img_array[0])
        #print("stylized image saved to disk..")

    def close(self):
        self.socket.close()
        self.context.close()


if __name__ == "__main__":
    image_url = "https://upload.wikimedia.org/wikipedia/commons/6/60/Naxos_Taverna.jpg"
    image_data = get_image_array(image_url)
    print("got image array")
    eclient = EffectClient()
    print("sending image data")
    eclient.send(image_data)
    print("waiting to recv")
    eclient.recv()
    print("closing..")
    # eclient.close()
    print("closed")
