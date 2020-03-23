# Training PyTorch CNN Benchmarks with DLRS + Intel® MKL-DNN

This directory contains code to train convolutional neural networks using cnn_benchmarks.

>IMPORTANT: To take advantage of the Intel® AVX-512 and VNNI functionality (including the MKL-DNN releases) with the Deep Learning Reference Stack, you must use the following hardware:
* Intel® AVX-512 images require an Intel® Xeon® Scalable Platform
* VNNI requires a 2nd generation Intel® Xeon® Scalable Platform
If not using such hardware, you should replace `FROM clearlinux/stacks-pytorch-mkl:v0.6.0` with `FROM clearlinux/stcks-pytorch-oss:v0.6.0` in the `Dockerfile`.

#### Pre-requisites:

* All steps in [Deploying Kubeflow with kfctl in Clear Linux OS]()

## Build Image

The PyTorch Job consumes a custom DLRS image for deployment. The default image name and tag is `repository/stacks-pytorch-kf-mkl:v0.6.0`; you should change the image name to match your project and make the proper changes in `pytorch_job_cnn_benchmarks.yaml`.

```bash
docker build -f Dockerfile -t project-name/stacks-pytorch-kf-mkl:v0.6.0 .
```

>NOTE: PyTorchJobs use docker image pull requests, thus the image built in the previous step should be available either on a local or remote registry. Please refer to the Kubernetes [documentation](https://kubernetes.io/docs/concepts/containers/images/) for more information.

## Submit a PyTorch Job for CNN Benchmarks

```bash
kubectl create -f ./pytorch_job_cnn_benchmarks.yaml
```

### You're ready

You should now see your master cluster running as well as worker pods (PyTorch Jobs) running benchmarking scripts.

To get the logs from each pod, run:
```bash
kubectl logs -n kubeflow -f <pod name>
```
