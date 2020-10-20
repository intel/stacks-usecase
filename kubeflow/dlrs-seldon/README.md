# Seldon Serving with Kubeflow and DLRS

Seldon Core is a wrapper that allows you to turn any model into a REST/GRPC microservice. Since it comes installed with Kubeflow, it is easy to start a SeldonDeployment on a Kubernetes cluster that has a Kubeflow deployment.
To learn more about Seldon, please refere to the official [documentation](https://docs.seldon.io/projects/seldon-core/en/latest/workflow/overview.html).
If you want to abstract the Kubeflow configuration and still have a model server in a kubernetes, please refer to the [DLRS + Seldon documentation]().

## Pre-requisites

- A running Kubeflow deployment as shown in the kubeflow/ directory

## Submitting a Model Server

The instructions below will show you how to create and submit a SeldonDeployment leveraging Kubeflow. A SeldonDeployment is a custom resource definition that allows you deploy your inference model to a Kubernetes cluster.

To learn more about the `SeldonDeployment` please refer to [SeldonDeployment](https://docs.seldon.io/projects/seldon-core/en/latest/workflow/overview.html#seldondeployment-crd).

1. Create a namespace where all your seldon deployments will be.

```bash
kubectl create namespace seldon
```

2. You have to label the previous namespace so that you can run inference

```bash
kubectl label namespace seldon serving.kubeflow.org/inferenceservice=enabled
```

3. Finally, you have to apply a deployment manifest with the SeldonDeployment definition, which resides inside a manifest like the following:

```yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: sample-model
spec:
  name: test-deployment
  predictors:
  - componentSpecs:
    - spec:
        containers:
        - image: sample-image
          name: classifier
    graph:
      children: []
      endpoint:
        type: REST
      name: classifier
      type: MODEL
    name: example
    replicas: 1
```

```bash
kubectl apply manifest.yaml
```

## Using DLRS as a model server

`seldon-core` comes installed with DLRS (all flavours), if you want to use DLRS as a model server, please refer to the [DLRS + Seldon documentation]() to get a deployment manifest that includes the DLRS custom image for model servers and use that in step three.
