# Docker image for running examples in Tensorflow models.
FROM sysstacks/dlrs-tensorflow-ubuntu:v0.7.0

RUN mkdir -p /opt
RUN git clone https://github.com/tensorflow/benchmarks.git /opt/tf-benchmarks

COPY launcher.py /opt
RUN chmod u+x /opt/*
ENTRYPOINT ["/opt/launcher.py"]
