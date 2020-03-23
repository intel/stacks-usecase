# Kubeflow Specific Files

This folder is home for kubeflow specific files to enable DLRS images with various workloads that exist as part of kubeflow. Long term plan would be to upstream some of these to kubeflow.

# Getting started with Kubeflow

>IMPORTANT: For troubleshooting, please refer to Kubeflow [documentation](https://www.kubeflow.org/docs/started/k8s/kfctl-k8s-istio/).

#### Pre-requisites:

* A running Kubernetes cluster (v1.17.1)

If running on Clearlinux, please refer to: [Run Kubernetes on Clear Linux OS](https://clearlinux.org/documentation/clear-linux/tutorials/kubernetes)

## Deploying Kubeflow with kfctl/kustomize

1. Get kfctl [v1.0.1](https://github.com/kubeflow/kfctl/releases/download/v1.0.1/kfctl_v1.0.1-0-gf3edb9b_linux.tar.gz) tarball, untar and add the binary path to your PATH if desired

2. Install Kubeflow resources
```bash
# Env variables needed for your deployment
export KF_NAME=<your choice of name for the Kubeflow deployment>
export BASE_DIR=<path to a base directory>
export KF_DIR=${BASE_DIR}/${KF_NAME}
export CONFIG_URI="https://raw.githubusercontent.com/kubeflow/manifests/v1.0-branch/kfdef/kfctl_k8s_istio.v1.0.1.yaml"
```

3. Set up and deploy Kubeflow
```bash
mkdir -p ${KF_DIR}
cd ${KF_DIR}
kfctl apply -V -f ${CONFIG_URI}
```

Deployment takes around 10 minutes (or more depending on the hardware) to be ready to use. After that you can do
```bash
kubectl get pods -n kubeflow
```
to list all the Kubeflow resources deployed and monitor their status.


## Deploying Kubeflow on Google Cloud Platform (GCP)

Kubeflow has excellent documentation on how to deploy on GCP [here](https://www.kubeflow.org/docs/gke/deploy/deploy-cli/). However, the [Deep Learning Reference Stack](https://clearlinux.org/stacks/deep-learning) (DLRS) utilizes hardware advancments that are only on certain Intel chips (Skylake), and there is no single document explaining how to specify a minimum chip during kubeflow deployment. Those instructions are provided here.

1. Choose a zone you want to deploy in that has Intel Skylake cpus. Zones are listed [here](https://cloud.google.com/compute/docs/regions-zones/).

2. Deploy Kubeflow normally as specified [here](https://www.kubeflow.org/docs/gke/deploy/deploy-cli/) but stop at section ["Set up and deploy Kubeflow"](https://www.kubeflow.org/docs/gke/deploy/deploy-cli/#set-up-and-deploy-kubeflow). Instead, navigate to section ["Alternatively, set up your configuration for later deployment"](https://www.kubeflow.org/docs/gke/deploy/deploy-cli/#alternatively-set-up-your-configuration-for-later-deployment). Then follow step 1.

3. In step 2, you are instructed to edit the configuration files. There are two changes required for a DLRS compatible GCP cluster, and they are detailed below.

4. Navigate to the gcp_config directory and open the cluster.jinja file. Change the cluster property "minCpuPlatform" from "Intel Broadwell" to "Intel Skylake". Note: you may notice there are two minCpuPlatform properties in the file. On of them is for gpu node pools, and not all cpu/gpu combinations are combatible. Leave the gpu property untouched, and we will disable gpu node pools in the next step.

5. Open the "cluster-kubeflow.yaml" file and change the "gpu-pool-max-nodes" property to 0.

6. Follow steps 3-4 of ["Alternatively, set up your configuration for later deployment"](https://www.kubeflow.org/docs/gke/deploy/deploy-cli/#alternatively-set-up-your-configuration-for-later-deployment).

That's it! you have a GCP cluster with Intel Skylake cpus.


# Kubeflow components

There is a list of Kubeflow components you can interact with. In this repository you will find a set of components using the System Stacks for different workloads:
- TfJobs
- PytorchJobs
- Jupyter Notebooks
- Seldon Model Server
- Pipelines
