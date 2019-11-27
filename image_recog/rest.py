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
"""a rest api for image recognition"""
#
#
#
import io

import quart

from PIL import Image
from quart_cors import cors

from main import classify

app = quart.Quart(__name__)
cors(app)


banner = {
    "what": "image recognition api",
    "usage": {
        "client": "curl -i  -X POST -F img=@data/cat.jpg 'http://localhost:5000/recog'",
        "server": "docker run -d -p 5000:5000 stacks_img_recog",
    },
}


@app.route("/usage", methods=["GET"])
def usage():
    return quart.jsonify({"info": banner}), 201


@app.route("/recog", methods=["POST"])
def recog():
    if quart.request.files.get("img"):
        img = quart.request.files["img"].read()
        img = Image.open(io.BytesIO(img))
        y_hat = classify(img)
        return quart.jsonify({"class": y_hat[0], "prob": y_hat[1]}), 201
    return quart.jsonify({"status": "not an image file"})


@app.errorhandler(404)
def not_found(error):
    return quart.make_response(quart.jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5059)
