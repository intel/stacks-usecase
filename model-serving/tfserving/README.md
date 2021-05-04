# Serving machine learning models with dlrs-serving

This document will guide you through the process of deploying a machine learning model with dlrs-serving and TensorFlow Serving.

### Software

* DLRS v0.9.0 with TensorFlow 2.4 (sysstacks/dlrs-tensorflow2-ubuntu:v0.9.0)
* DLRS v0.9.0 with TensorFlow Serving 2.4 (sysstacks/dlrs-serving-ubuntu:v0.9.0)
* Prometheus 2.23
* Docker 18 or above

> Important: To be able to run these steps, you must ensure your hardware has Intel AVX-512 enabled.

## Preparing your model

To be able to load  a trained model into TensorFlow Serving, it must be saved in TensorFlow's `SavedModel` format, which contains a TensorFlow complete program, including weights and computation, and does not require to have the original model building code to run.

Append the following lines to your model building code:

```bash
# Assuming import tensorflow as tf
# and the model variable points to the trained model

MODEL_DIR = “/workspace”
version = 1
export_path = os.path.join(MODEL_DIR, str(version))

tf.keras.models.save_model(
    model,
    export_path,
    overwrite=True,
    include_optimizer=True,
    save_format=None,
    signatures=None,
    options=None
)
```

These lines will create a SavedModel using TensorFlow Keras API after the training process is completed.

## Training a model with DLRS and TensorFlow 2.4

For the sake of simplicity, the training algorithm won’t be shown in this section. The important thing to notice is that besides saving the model, no significant changes have to be made on the traditional training algorithm and code, in fact, up to this point everything should be done as usual.

In this directory you will find `Dockerfile.training` and `training_entrypoint.sh`, these files will allow you to build and run a DLRS container image that will train and save your model in the correct format. Before running the following commands, make sure your model building is inside tfserving/shared.

1. Build the training image

```bash
$ pwd
<some path>/stacks-usecase/model-serving/tfserving/
$ docker build -t dlrs-training:v0.1 -f Dockerfile.training .
```

2. Train and save

```bash
$ docker run --rm -v ${PWD}/shared:/workspace dlrs-training:v0.1

# The output of your model building code should appear:
Downloading data from https://storage.googleapis.com/tensorflow/tf-keras-datasets/train-labels-idx1-ubyte.gz
32768/29515 [=================================] - 0s 2us/step
…
Epoch 1/5
1210/1875 [==================>...........] - ETA: 46s - loss: 0.7991 - accuracy: 0.7250
…
```

3. Check the SavedModel. The `1/` directory contains the SavedModel object and it is now to be loaded to a model server. The 1 represents the version number. This will be useful in future steps.

```bash
$ ls shared/models

1/ 
```

## Serving a model with dlrs-serving and TensorFlow Serving 2.4

Once saved, the model can be loaded into a model server. dlrs-serving provides the environment for running a model server with TensorFlow Serving. In this section, dlrs-serving will be used for building a serving container image.

> NOTE: This guide will show how to serve through a REST API. TensorFlow Serving also allows users to do it through gRPC. Please refer to TensorFlow Serving documentation for details on other options. 

1. Build the serving image

```bash
$ docker build -t dlrs-serving:v0.1 -f Dockerfile.serving .
```

2. Run and deploy

```bash
$ docker run --rm -v ${PWD}/shared/models/:/models -p 8501:8501 -e MODEL_NAME=<model_name> dlrs-serving:v0.1

# The output of the model server should appear:
2020-12-04 17:49:01.230807: I tensorflow_serving/core/loader_harness.cc:87] Successfully loaded servable version {name: model_name version: 1}
[evhttp_server.cc : 238] NET_LOG: Entering the event loop ...
2020-12-04 17:49:01.313477: I tensorflow_serving/model_servers/server.cc:387] Exporting HTTP/REST API at:localhost:8501 ...

```

Your model server is now running and you are able to make POST requests to `http://localhost:8501/v1/models/model_name/versions/1:predict` for predictions.

## Advanced configuration

TensorFlow Serving provides a model server ready for production, it is a powerful tool that can be configured using configuration files that will be read and interpreted in runtime to influence the behaviour of the server.

### Serving multiple models

TensorFlow Serving is capable of serving multiple models on a single server. To enable this capability, you can specify a `model_config_file` as in the one provided in `config/multi_models.conf`. Please make sure that your saved models reside in `shared/models/`.

1. Use the template in `config/multi_models.conf` and adapt it to your needs.

2. Comment out the first block of code in `scripts/serving_entrypoint.sh` and uncomment the second block, so that the only uncommented lines are the following:

```bash
tensorflow_model_server --rest_api_port=8501 \
       --model_config_file=/models/multi_models.conf \
       "$@"
```

3. Re-build the serving image

```bash
$ docker build -t dlrs-serving:v0.2 -f Dockerfile.serving .
```

4. Run the container image again. You will be able to make requests to each of the models you uploaded by pointing to the model name.

```bash
$ docker run --rm -v ${PWD}/shared/models/:/models -p 8501:8501 dlrs-serving:v0.2

# For model_a --> http://localhost:8501/v1/models/model_a/versions/1:predict 
# For model_b --> http://localhost:8501/v1/models/model_b/versions/1:predict 

# You should be able to see both models loaded:
...
2020-12-07 22:13:19.619699: I tensorflow_serving/core/loader_harness.cc:74] Loading servable version {name: model_a version: 1}
2020-12-07 22:13:19.519714: I tensorflow_serving/core/loader_harness.cc:74] Loading servable version {name: model_b version: 1}
2020-12-07 22:13:19.730794: I tensorflow_serving/model_servers/server.cc:387] Exporting HTTP/REST API at:localhost:8501
```

### Serving multiple versions

Similarly to serving multiple models, you can serve multiple versions of a single model by creating a configuration file.

1. Use the template in `config/multi_versions.conf` and adapt it to your needs.

2. Comment out the first two blocks of code in `scripts/serving_entrypoint.sh` and uncomment the third block, so that the only uncommented lines are the following:

```bash
tensorflow_model_server --rest_api_port=8501 \
       --model_name=${MODEL_NAME} --model_base_path=${MODEL_DIR} \
       --model_config_file=/models/multi_versions.conf \
       --allow_version_labels_for_unavailable_models=true \
       "$@"
```

3. Re-build the serving image

```bash
$ docker build -t dlrs-serving:v0.3 -f Dockerfile.serving .
```

4. Run the container image again. You will be able to make requests to each of the models you uploaded by pointing to the model name.

```bash
$ docker run --rm -v ${PWD}/shared/models/:/models -p 8501:8501 dlrs-serving:v0.3

# For my_model v1 --> http://localhost:8501/v1/models/my_model/versions/1:predict
# Or by its label --> http://localhost:8501/v1/models/my_model/labels/stable:predict
# For my_model v2 --> http://localhost:8501/v1/models/my_model/versions/2:predict
# Or by its label --> http://localhost:8501/v1/models/my_model/labels/dev:predict
```

### Monitoring

TensorFlow Serving provides a way of monitoring the server using the `--monitoring_config_file` flag and specifying a monitor configuration file. This configuration allows users to read metrics from the server, such as the number of times the model was attempted to load, number of requests, among many others. TensorFlow Serving collects all metrics that are captured by Serving as well as core TensorFlow. To enable server monitoring, a Prometheus server that pulls metrics from the model server is required.

#### Pre-requisites

* Prometheus 2.23 or higher installed

1. Run a Prometheus server using the `config/prometheus.yml` file already provided. It already points to the model server created in previous steps.

2. We have provided a configuration file for monitoring in `config/monitoring.conf` and it will be used in following steps.

3. Comment out the first three blocks of code in `scripts/serving_entrypoint.sh` and uncomment the last block, so that the only uncommented lines are the following:

```bash
tensorflow_model_server --rest_api_port=8501 \
       --model_name=${MODEL_NAME} --model_base_path=${MODEL_DIR}/ \
       --monitoring_config_file=/models/monitoring.conf \
        "$@"
```

4. Re-build the serving image.

```bash
$ docker build -t dlrs-serving:v0.4 -f Dockerfile.serving .
```

5. Run the container image again. You will be able to make requests to each of the models you uploaded by pointing to the model name.

```bash
$ docker run --rm -v ${PWD}/shared/models/:/models -p 8501:8501 dlrs-serving:v0.4
```

You should now be able to access the Prometheus web UI to monitor your model server. You can watch metrics by typing `:tensorflow:core` for TensorFlow core metrics or `:tensorflow:cc` in the search bar.
