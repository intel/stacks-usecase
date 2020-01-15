# Handwritten Digit Recognition with DLRS

The content in this directory is for running a handwritten digit recognition example using the Deep Learning Reference Stack, Pytorch and MNIST.

#### Pre-requisites

* Docker

## Running on containers

Please follow these instructions to train the model and classify random handwritten digits on DLRS based Docker containers.

### Set up 

Set TYPE and REGISTRY env variables
TYPE options: mkl or oss
REGISTRY options: registry name

```bash
export TYPE=<oss or mkl>
export REGISTRY=<your registry>
make
```

### Train

```bash
mkdir models
docker run --rm -ti -v ${PWD}/models:/workdir/models $REGISTRY/dlrs-train-$TYPE:latest "-s train"
```

### Serving the model for live classification

```bash
docker run -p 5059:5059 -it -v ${PWD}/models:/workdir/models $REGISTRY/dlrs-serve-$TYPE:latest "-s serve"
curl -i -X POST -d 'Classify' http://localhost:5059/digit_recognition/classify
```

### Website

We have created a simple website template for you to interact with.

```bash
docker run --rm -p 8080:5000 -it $REGISTRY/dlrs-website:latest --website_endpoint 0.0.0.0
Open localhost:8080 on a web browser
```

## Running on Kubeflow pipelines

We have created a Kubeflow Pipeline to run this example. Please go to [Kubeflow Pipelines](https://github.com/intel/stacks-usecase/kubeflow/pipelines) for more details.
