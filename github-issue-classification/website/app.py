#!/usr/bin/env python
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

"""webserver for the github-issue-classifier"""

import argparse

import requests
from flask import Flask
from flask import request
from flask import render_template

app = Flask("website for github issue classifier example")
parser = argparse.ArgumentParser()
parser.add_argument("-ip", "--endpoint", required=False,
                    default="localhost", help="Endpoint address of the inference API")
parser.add_argument("-p", "--port", required=False,
                    default="5059", help="Endpoint port of the inference API")
parser.add_argument("-wip", "--website_endpoint", required=False,
                    default="localhost", help="Endpoint address for the website")
parser.add_argument("-wp", "--website_port", required=False,
                    default="5000", help="Endpoint port for the website")
parser.add_argument("-s", "--tls", required=False, action="store_true",
                    default=False, help="Is the inference endpoint encrypted with TLS ")
args = vars(parser.parse_args())


@app.route("/", methods=["GET", "POST"])
def homepage():
    args["protocol"] = "https" if args["tls"] else "http"
    input_text = None
    if request.method == "POST":
        input_text = request.form["inputText"]
        response = requests.post("{}://{}:{}/github_issues/infer".format(
            args["protocol"], args["endpoint"], args["port"]), json={"issue": str(input_text)})
        labels_json = response.json()
        labels = ", ".join(labels_json["label"][0])
        return render_template("homepage.html", outText="You submitted {}".format(input_text), optText=labels)
    return render_template("homepage.html", outText=None, optText=None)


if __name__ == "__main__":
    app.run(debug=False, host="{}".format(
        args["website_endpoint"]), port=int(args["website_port"]))
