#!usr/bin/env python
#
# Copyright (c) 2019 Intel Corporation
#
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
"""A REST API for Pytorch MNIST Handwritten Digit Recognition"""

import flask

from classify import classify

app = flask.Flask("Handwritten Digit Recognition")

banner = {
    "what": "Handwritten Digit Recognition",
    "usage": {
        "Client": "curl -i -X POST -d 'Classify' http://localhost:5059/digit_recognition/classify",
        "Server": "docker run -d -p 5059:5059 stacks_handwritten_digit_recog",
    },
}


@app.route("/digit_recognition/", methods=["GET"])
def index():
    return flask.jsonify(banner), 201


@app.route("/digit_recognition/classify", methods=["POST"])
def digit_recog():
    img, probab = classify(imgshow=False)
    return flask.jsonify({"Prediction": probab.index(max(probab))}), 201


@app.errorhandler(404)
def not_found(error):
    return flask.make_response(flask.jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5059)
