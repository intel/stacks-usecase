# Seldon and OpenVINO model server using the Deep Learning Reference Stack

[Seldon Core](https://docs.seldon.io/projects/seldon-core/en/latest/) is an open source platform for deploying machine learning models on a Kubernetes cluster.

#### Pre-requisites:

* A running Kubernetes cluster

Please refer to: [Run Kubernetes on Clear Linux OS](https://clearlinux.org/documentation/clear-linux/tutorials/kubernetes)

* An existing Kubeflow deployment

## Install deployment tools

```bash
INSTALL_DIR=$HOME/install_dir
BIN_DIR=${INSTALL_DIR}/bin
SRC_DIR=${INSTALL_DIR}/source
export PATH=${BIN_DIR}:$PATH

mkdir -p ${BIN_DIR} && mkdir ${SRC_DIR}
cd ${SRC_DIR}
```

#### Helm

```bash
wget https://get.helm.sh/helm-v2.14.3-linux-amd64.tar.gz && tar xf helm-v2.14.3-linux-amd64.tar.gz
mv linux-amd64/helm ${BIN_DIR}/helm
```

#### Clean environment

```bash
rm -rf ${SRC_DIR}/*
```

## Prepare DLRS image

First of all, a base image with Seldon + OpenVINO inference engine should be created using `Dockerfile_openvino_base`.

```bash
docker build -f Dockerfile_openvino_base -t dlrs_openvino_base:0.1 .
```

## Mount pre-trained models into a persistent volume
Apply all PV manifests to the cluster

```bash
kubectl apply -f storage/pv-volume.yaml
kubectl apply -f storage/model-store-pvc.yaml
kubectl apply -f storage/pv-pod.yaml	
```

Get a shell to the container used as pv:

```bash
kubectl exec -it hostpath-pvc -- /bin/bash
```

Once you're inside the running container, fetch your pre-trained models and save them at `/opt/ml` :

```bash
root@hostpath-pvc:/# cd /opt/ml
root@hostpath-pvc:/# # Copy your models here
root@hostpath-pvc:/# # exit
```

## Deploy the model server

Now you're to deploy the model server using the Helm chart provided.

```bash
helm install --name=seldonov-model-server \
    --namespace kubeflow \
    --set openvino.image=dlrs_openvino_base:0.1 \
    --set openvino.model.path=/opt/ml/<models_directory> \
    --set openvino.model.name=<model_name> \
    --set openvino.model.input=data \
    --set openvino.model.output=prob
    dlrs-seldon/helm/seldon-model-server 
```

## Extended example

#### Install source to image (s2i)

```bash
cd ${SRC_DIR}
wget https://github.com/openshift/source-to-image/releases/download/v1.1.14/source-to-image-v1.1.14-874754de-linux-amd64.tar.gz
tar xf source-to-image-v1.1.14-874754de-linux-amd64.tar.gz
mv s2i ${BIN_DIR}/s2i && ln -s s2i ${BIN_DIR}/sti
```

#### Clone seldon-core

```bash
git clone https://github.com/SeldonIO/seldon-core.git ${SRC_DIR}/seldon-core
```

Using the DLRS image created above, you can build an image for deploying the Image Transformer component that consumes imagenet classification models.

```bash
cd ${SRC_DIR}/seldon-core/examples/models/openvino_imagenet_ensemble/resources/transformer/
s2i -E environment_grpc . dlrs_openvino_base:0.1 imagenet_transformer:0.1
```

You can now use this newly created image for deploying the Image Transformer component of the [OpenVINO imagenet pipelines example](https://docs.seldon.io/projects/seldon-core/en/stable/examples/openvino_ensemble.html)
