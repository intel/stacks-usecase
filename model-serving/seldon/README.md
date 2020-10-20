# DLRS + Seldon Core

Seldon Core allows you to convert any machine learning model into production REST/GRPC microservice. You can use `seldon-core` to deploy anywhere: cloud services, on-prem, and in a Kubernetes cluster.

There are two ways of using Seldon Core:

1. Pre-packaged model servers. These are provided by Seldon and have a generic docker image to run inference.
2. Reusable/Non-reusable model servers. These are modified and built by the user and can have a specialized and optimized image, such as DLRS. The final goal is to containerize the model using a language wrapper.

The scope of this guide is to show how you can integrate DLRS with Seldon Core to build and deploy a model server, thus we'll use the second method.

### Containerize using language wrappers

Seldon Core language wrappers allows the user to create reusable and non-reusable model servers. There is a large list of supported languages, this guide uses the Python wrapper.

> Reusable: downloads the pretrained model from remote repository
Non-reusable: loads model from a file embedded in the image

The containerization process is fairly easy, as you have to:

1. Encapsulate your inference logic into a Python class. Example:

```python
class Model():
    def __init__(self)
        self.model = # Here is where you would load your model
    def prediction(self,...):
        # Here is where you would add the inference logic and return a prediction
        return self.model.predict(...)
```

2. Create a container image that includes your model class from the previous step and that runs the `seldon-core-microservice`. Since DLRS already comes with `seldon-core` it is very easy to just set up:

```Dockerfile
FROM sysstacks/dlrs-tensorflow-ubuntu:v0.7.0
WORKDIR /model-server
COPY Model.py
EXPOSE 5000

# Define environment variable
ENV MODEL_NAME MyModel
ENV API_TYPE REST
ENV SERVICE_TYPE MODEL

CMD exec seldon-core-microservice $MODEL_NAME $API_TYPE --service-type $SERVICE_TYPE
```

To build the above image, run:

```bash
docker build -t repository/my-model-server:0.1
```

Up to this point you can use your container image to turn your local machine into a model server by running the image and making POST requests to it. This step will show you how to deploy your model server as a SeldonDeployment in a Kubernetes cluster. Make sure you meet the pre-requisites listed in this guide.

3. Create a deployment manifest in which you specify the container image created in the previous step and submit it to the Kubernetes cluster.

```yaml
apiVersion: machinelearning.seldon.io/v1alpha2
kind: SeldonDeployment
metadata:
  name: seldon-deployment-example
spec:
  name: sklearn-iris-deployment
  predictors:
  - componentSpecs:
    - spec:
        containers:
        - image: repository/my-model-server:0.1
          imagePullPolicy: IfNotPresent
          name: sklearn-iris-classifier
    graph:
    ...
```

4. You can now make inference requests to the REST/GRPC API.

## DLRS Example

* [Hello Seldon]()
