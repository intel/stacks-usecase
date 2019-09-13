# Github Issue Classification running on Kubernetes

## Pre-requisites
1. k8s deployment
2. kubeflow v0.6.1 deployment

## Initial setup

```bash
WORKDIR="<path to a local workdir>"
GIC_WORKDIR="${WORKDIR}/usecases/tensorflow/github-issue-classification/"
git clone https://github.com/intel/stacks-usecase.git $WORKDIR/usecases
cd $GIC_WORKDIR/

# This script assumes you are on a Clearlinux host for installig jq
# If you are on a different host, please install jq using your
# distro package manager
./scripts/get-data.sh -u
```

## Create a PV

```bash
# Load a PV on the kubeflow namespace
kubectl apply -f $GIC_WORKDIR/k8s/storage/tfevent-pv.yaml
kubectl apply -f $GIC_WORKDIR/k8s/storage/tfevent-pvc.yaml
kubectl apply -f $GIC_WORKDIR/k8s/storage/tfevent-pod.yaml

# Create needed directories
kubectl exec -ti tfevent-pod -n kubeflow -- /bin/bash

# Once inside the PV container
root@tfevent-pod:/ mkdir -p /workdir/data/raw
root@tfevent-pod:/ mkdir -p /workdir/training
root@tfevent-pod:/ exit

# Copy all needed files into the PV
kubectl cp $GIC_WORKDIR/python/train.py kubeflow/tfevent-pod:/workdir/training
kubectl cp $GIC_WORKDIR/data/raw/all_issues.json kubeflow/tfevent-pod:/workdir/data/raw
kubectl cp $GIC_WORKDIR/scripts/proc-data.scala kubeflow/tfevent-pod:/workdir/data
```

## Data pre-processing

```bash
# Deploy dars container for pre-proc
kubectl apply -f $GIC_WORKDIR/k8s/manifests/process-data.yaml
```

## Model training

> NOTE: To take advantage of the Intel® AVX-512 and VNNI functionality
(including the MKL-DNN releases) with the Deep Learning Reference Stack,
you must use the following hardware:
*Intel® AVX-512 images require an Intel® Xeon® Scalable Platform
*VNNI requires a 2nd generation Intel® Xeon® Scalable Platform

```bash
# Build a Docker image to be consumed by the TfJob. Note the image should be
# available at a registry where your kubernetes deployment has access to
cd $GIC_WORKDIR/docker
docker build -f Dockerfile.train -t <your-registry>/stacks-dlrs-mkl-gic:v0.4.1 .
docker push <your-registry>/stacks-dlrs-mkl-gic:v0.4.1

# Edit the TFJob manifest at (k8s/manifests/tf_job_github.yaml) to
# match your registry in all the fields that apply:
image: <your-registry>/stacks-dlrs-mkl-gic:v0.4.1

# Create a TFJob for training the model
cd $GIC_WORKDIR/k8s
kubectl create -f manifests/tf_job_github.yaml
```

## Inference

```bash
# Build a Docker image to be consumed by the inference pod. Note the image should
# be available at a registry where your kubernetes deployment has access to
cd $GIC_WORKDIR/docker
docker build -f Dockerfile -t <your-registry>/stacks-dlrs-mkl-inference:v0.4.1 ..
docker push <your-registry>/stacks-dlrs-mkl-inference:v0.4.1

# Edit the inference pod manifest at (k8s/manifests/inference-pod.yaml) to
# match your registry in all the fields that apply:
image: <your-registry>/stacks-dlrs-mkl-inference:v0.4.1

# Create an inference pod
cd $GIC_WORKDIR/k8s
kubectl create -f manifests/inference-pod.yaml
```
