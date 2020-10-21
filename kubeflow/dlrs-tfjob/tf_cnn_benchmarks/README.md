# Training Tensorflow CNN Benchmarks with DLRS + Intel® OneDNN and AVX512-DL Boost

This directory contains code to train convolutional neural networks using [tf_cnn_benchmarks](https://github.com/tensorflow/benchmarks/tree/master/scripts/tf_cnn_benchmarks).

> Source: [Training TF CNN models](https://github.com/kubeflow/kubeflow/tree/v1.1-branch/tf-controller-examples/tf-cnn)

>IMPORTANT: To take advantage of the Intel® AVX-512 and VNNI functionality with the Deep Learning Reference Stack, you must use the following hardware:
* Intel® AVX-512 images require an Intel® Xeon® Scalable Platform
* VNNI requires a 2nd generation Intel® Xeon® Scalable Platform

#### Pre-requisites:

* All steps in [Deploying Kubeflow with kfctl](https://github.intel.com/verticals/usecases/tree/master/kubeflow/dlrs-tfjob#deploying-kubeflow-with-kfctl)


## Build Image

The TFJob consumes a custom DLRS image for deployment. The default image name and tag is `repository/dlrs-tensorflow-kf:v0.7.0`; you should change the image name to match your project and make the proper changes in `tf_job_cnn_benchmarks.yaml`.

```bash
docker build -f Dockerfile -t repository/dlrs-tensorflow-mkl:v0.7.0 .
```

>NOTE: TFJobs use docker image pull requests, thus the image built in the previous step should be available either on a local or remote registry. Please refer to the Kubernetes [documentation](https://kubernetes.io/docs/concepts/containers/images/) for more information.

## Submit a TFJob for TF CNN Benchmarks

```bash
kubectl create -f ./tf_job_cnn_benchmarks.yaml
```

### You're ready

You should now see your master cluster running as well as worker pods (TFJobs) running benchmarking scripts.

To get the logs from each pod, run:
```bash
kubectl logs -n kubeflow -f <pod name>
```
