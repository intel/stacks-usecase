# Hello Seldon example

In this example we will guide you through the model wrapping process and containerization. The "model" we are using is not an actual model, but a printing example, the intention is just to showcase seldon and DLRS capabilities, please use this as a template for your model.

## Pre-requisites

* Kubernetes cluster (v1.14 or above)
* `seldon-core-operator` latest [installed](https://docs.seldon.io/projects/seldon-core/en/latest/workflow/install.html)
* Istio ingress latest [installed](https://istio.io/latest/docs/setup/install/operator/)
* Istio gateway for seldon [installed](https://docs.seldon.io/projects/seldon-core/en/latest/ingress/istio.html)

## Wrap a model

Pre-trained model loading and inference logic should be defined as a Python class. Create `MyModel.py` as follows:
```python
class MyModel():
   def __init__(self):
       """
       All initialization parameters go here. Your model should be loaded in this section.
       """

       print("Init")
   def predictor(self):
       """
       This method returns a prediction.
       """

       print("A prediction called is received - Returning a prediction")
       return "Prediction - Hello Seldon"
```

## Containerize your model server

Define a Dockerfile in the same directory where `MyModel.py` is as it will be copied inside the container image. Create a `Dockerfile` with DLRS as parent as follows:

> NOTE: All DLRS flavours have `seldon-core` installed already, so you can use any in your deployments depending on your needs.

```Dockerfile
FROM sysstacks/dlrs-tensorflow-ubuntu:v0.7.0
WORKDIR /model-server
COPY . .
EXPOSE 5000

# Define environment variable
ENV MODEL_NAME MyModel
ENV API_TYPE REST
ENV SERVICE_TYPE MODEL
ENV PERSISTENCE 0

CMD exec seldon-core-microservice $MODEL_NAME $API_TYPE --service-type $SERVICE_TYPE --persistence $PERSISTENCE
```

You can build the image with the following command:

```bash
docker build -t repository/dlrs-serving:v0.1
```

## SeldonDeployment

The final step is to create a deployment manifest and apply it to a running Kubernetes cluster. You can use the template included in this directory. Make sure that `image` and `name` correspond to your project specifics.

For example:

```yaml
apiVersion: machinelearning.seldon.io/v1alpha2
kind: SeldonDeployment
metadata:
  name: hello-seldon
spec:
  name: hello-seldon-deployment
  predictors:
  - componentSpecs:
    - spec:
        containers:
        - image: repository/dlrs-serving:v0.1
          imagePullPolicy: IfNotPresent
          name: classifier
    graph:
      children: []
      endpoint:
        type: REST
      name: classifier
      type: MODEL
    name: default
    replicas: 1
```

Submit your SeldonDeployment with `kubectl apply -f hello-seldon.yaml`.

## Testing model endpoints

Since we defined this example to serve in a REST endpoint, we can make prediction calls as follows:

```bash
curl -X POST http://<ingress>/seldon/default/hello-seldon/api/v1.0/predictions
```

For deployments using the Istio gateway (as this one), the `<ingress>` path is usually `localhost:80`. For troubleshooting, please refer to Seldon official documentation for [testing your model endpoints](https://docs.seldon.io/projects/seldon-core/en/latest/workflow/serving.html).
