#Copyright (c) 2021, Intel Corporation.
#SPDX-License-Identifier: BSD-3-Clause


FROM sysstacks/dlrs-tensorflow2-ubuntu:latest
#FROM ubuntu:focal

COPY . /workspace

# Set the PYTHONPATH to finish installing the API
ENV PYTHONPATH=$PYTHONPATH:/models/research/object_detection
ENV PYTHONPATH=$PYTHONPATH:/models/research/slim
ENV PYTHONPATH=$PYTHONPATH:/models/research
ENV POETRY_VIRTUALENVS_CREATE=false

# docker image stub
RUN DEBIAN_FRONTEND="noninteractive" apt-get update && apt-get -y upgrade && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends apt-utils && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y libgl1-mesa-glx git && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y build-essential protobuf-compiler curl unzip && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y python-pil python-lxml python-tk python3-dev python3-opencv python3-pip

# clone the repository 
RUN git clone --depth 1 https://github.com/tensorflow/models.git

# Get protoc 3.0.0, rather than the old version already in the container
RUN curl -OL "https://github.com/google/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip" && \
    unzip protoc-3.0.0-linux-x86_64.zip -d proto3 && \
    mv proto3/bin/* /usr/local/bin && \
    mv proto3/include/* /usr/local/include && \
    rm -rf proto3 protoc-3.0.0-linux-x86_64.zip

# Run protoc on the object detection repo
RUN cd models/research && \
    protoc object_detection/protos/*.proto --python_out=. && \
    cp -r object_detection /workspace/src/effects_service

# set model detection utils in python path
RUN echo "export PYTHONPATH=$PYTHONPATH:/models/research/object_detection" >> ~/.bashrc &&\
    echo "export PYTHONPATH=$PYTHONPATH:/models/research/slim" >> ~/.bashrc &&\
    echo "PYTHONPATH=$PYTHONPATH:/models/research" >> ~/.bashrc

WORKDIR /workspace/src/effects_service

# install deps for the object detection model as well
RUN cd /workspace && \
    pip install --no-cache-dir -U poetry && \
    poetry install

ENTRYPOINT [ "poetry", "run", "python3", "api.py" ]
