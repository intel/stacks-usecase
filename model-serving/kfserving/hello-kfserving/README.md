# Hello KFServing example

In this example we will guide you through the model preparation process and containerization. The "model" we are using is not an actual model, but an example showing a skeleton, the goal is just to showcase KFServing and DLRS capabilities, please use this as a template for your model.

## Pre-requisites

* Kubernetes cluster (v1.14 or above)
* Kubeflow (v1.0 or above) installed in a Kubernetes cluster
* KFServing [installed](https://github.com/kubeflow/kfserving/#kfserving-in-kubeflow-installation) in Kubeflow

## Prepare your model

As mentioned, a pre-trained model loading and inference logic should be defined as a Python class. Create `MyModel.py` as follows:
```python
import kfserving

class MyModel(kfserving.KFModel):
   def __init__(self, name: str):
       super().__init__(name)
       """
       All initialization parameters go here. Your model should be loaded in this section.
       """
       print("Init")
   def load(self):
       """
       This method will include loading instructions for your model
       """
       print("Model is loaded")
   def predictor(self):
       """
       This method returns a prediction, add all the prediction logic here.
       """
       print("A prediction called is received - Returning a prediction")
       return "Prediction - Hello Seldon"
if __name__=="__main__":
    model = MyModel("name-of-my-model")
    model.load()
    kfserving.KFServer(workers=1).start([model])
```

## Containerize your model server

Define a Dockerfile in the same directory where `MyModel.py` is as it will be copied inside the container image. Create a `Dockerfile` with DLRS as parent as follows:

> NOTE: All flavours of DLRS can be used here, choose one depending on your needs.

```Dockerfile
FROM sysstacks/dlrs-tensorflow-ubuntu:v0.9.0
WORKDIR /model-server
RUN pip install --no-cache-dir kfserving

COPY MyModel.py .
# You should copy any dependencies for your model (like labels)

CMD ["python", "MyModel.py"]
```

You can build the image with the following command:

```bash
docker build -t repository/dlrs-serving:v0.1
```

## InferenceService

The final step is to create a deployment manifest and apply it to a running Kubernetes cluster. You can use the template included in this directory. Make sure that `image` and `name` correspond to your project specifics.

For example:

```yaml
apiVersion: serving.kubeflow.org/v1alpha2
kind: InferenceService
metadata:
  labels:
    controller-tools.k8s.io: "1.0"
  name: dlrs-kfserving
spec:
  default:
    predictor:
      custom:
        name: custom
        container:
          image: repository/dlrs-serving:v0.1
          imagePullPolicy: IfNotPresent
```

Submit your InferenceService with `kubectl apply -f hello-kfserving.yaml`.

## Testing model endpoints

This example will serve in a REST endpoint, we can make prediction calls as follows:

```bash
MODEL_NAME=dlrs-kfserving
SERVICE_HOSTNAME=$(kubectl get inferenceservice ${MODEL_NAME} -o jsonpath='{.status.url}' | cut -d "/" -f 3)

curl -v -H "Host: ${SERVICE_HOSTNAME}" http://${INGRESS_HOST}:${INGRESS_PORT}/v1/models/${MODEL_NAME}:predict -d <data, this can be a path to a JSON file>
```

For deployments using the Istio gateway (as this one), the `<INGRESS_HOST>` path is usually `localhost:80`. For troubleshooting, please refer to Kubeflow official documentation for [Determine the ingress IP and ports](https://github.com/kubeflow/kfserving/blob/master/README.md#determine-the-ingress-ip-and-ports)
