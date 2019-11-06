#!usr/bin/env python
#
# Copyright (c) 2019 Intel Corporation
#
# Main author:
#   * unrahul <rahul.unnikrishnan.nair@intelcom>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""a rest api for pix2pix."""
import io
import random
import string

import flask
from PIL import Image

from infer import infer

app = flask.Flask("pix2pix api")


banner = {
    "what": "pix2pix api",
    "usage": {
        "client": "curl -i  -X POST -F img=@data/abstract.jpg 'http://localhost:5000/generate'",
        "server": "docker run -d -p 5000:5000 pix2pix-infer",
    },
}


@app.route("/usage", methods=["GET"])
def usage():
    return flask.jsonify({"info": banner}), 201


@app.route("/generate", methods=["POST"])
def generate():
    """generate an image from an `img` obtained from a post request"""
    if flask.request.files.get("img"):
        img = flask.request.files["img"].read()
        image = Image.open(img).convert("RGB")
        input_img_path = "input_img_{}.jpg".format("".join(random.choices(string.ascii_letters, k=5)))
        image.save(input_img_path)
        y_hat = infer(input_img_path)
        return flask.jsonify({"generated": y_hat}), 201
    return flask.jsonify({"status": "not an image file"})


@app.errorhandler(404)
def not_found(error):
    return flask.make_response(flask.jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5059)
