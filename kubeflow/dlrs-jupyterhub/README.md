# JupyterHub with Kubeflow and DLRS

The Deep Learning Reference Stack (DLRS) has jupyterhub enabled, but to use it with Kubeflow and JupyterHub requires slight modification.

#### Pre-requisites:

* Docker, or your container builder of choice
* An image registry, ie Google’s GCR, AWS’s ECR, Azure’s CR, or a private registry
* A working instance of Kubeflow
* A running Kubernetes cluster

Please refer to: [Run Kubernetes on Clear Linux OS](https://clearlinux.org/documentation/clear-linux/tutorials/kubernetes)
Also refer to: [Installing Kubeflow](https://www.kubeflow.org/docs/started/getting-started)


## Deploying JupyterHub with DLRS
To prepare an image that can be used with JupyterHub, create an image using DLRS as a base and the JupyterHub startup commands as described below. There are multiple DLRS images to choose from, so be sure to find what works best for you. In this guide, we will use TensorFlow with Intel® OpenVINO, AVX 512 and Intel ® DL Boost.

1. Create a file named “Dockerfile” With these contents:

```bash
FROM clearlinux/stacks-dlrs-mkl:v0.6.0

ENV NB_PREFIX /
RUN mkdir /home/jovyan
CMD ["sh","-c", "jupyter notebook --notebook-dir=/home/jovyan --ip=0.0.0.0 --no-browser --allow-root --port=8888     --NotebookApp.token='' --NotebookApp.password='' --NotebookApp.allow_origin='*' --NotebookApp.base_url=${NB_PREFIX}"]
```

2. Inside the same directory as your file, run:

```bash
docker build -f Dockerfile -t jupyterhub-dlrs  .
```

3. Once your image is built, push the image to your image repository of choice. The commands will vary based on your repository, but a generic example looks like this:

```bash
docker push jupyterhub-dlrs
```

4. Follow the [JupyterHub documentation](https://www.kubeflow.org/docs/notebooks/setup/#install-kubeflow-and-open-the-kubeflow-ui) to set up your notebook server. Make sure to choose "custom image" and input the name of your container image.
