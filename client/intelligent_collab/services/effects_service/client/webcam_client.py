'''
This file is an example on how to consume the inference service
'''
import socket
import cv2

import msgpack
import msgpack_numpy as mn
import zmq


def send(socket, img_array):
    """send msg using client."""
    packed_image = msgpack.packb(img_array, default=mn.encode)
    socket.send(packed_image)

def recv(socket):
    packed_effect_image = socket.recv()
    print("recieved")
    img_array = msgpack.unpackb(packed_effect_image, object_hook=mn.decode)
    return img_array

def main():
    cam = cv2.VideoCapture(0)

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5555")
    if not cam.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        ret, image = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        image = cv2.flip(image, 1)

        send(socket, image)
        print("Request send, waiting for reply")
        image = recv(socket)
        print(f"Received reply {image.shape}")

        cv2.imshow('webcam', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()