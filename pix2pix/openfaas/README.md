# Pix2Pix on OpenFaaS

## Prerequisites

* `faas-cli` installed. Please refer to OpenFaaS [documentation](https://docs.openfaas.com/deployment/kubernetes/#install-the-faas-cli)

>NOTE: If you'r host OS is clearlinux, you can run `swupd bundle-add faas-cli` to install the OpenFaaS CLI.

* A running instance of OpenFaaS. Please refer to OpenFaaS [documentation](https://docs.openfaas.com/deployment/).

* A local copy of the System Stacks use cases repository.

```bash
$ git clone https://github.com/intel/stacks-usecase.git
```

## Deploy Pix2Pix using faas-cli

### Setting your environment

#### DLRS for OpenFaaS template

You should first pull the DLRS template for OpenFaaS

>NOTE: The template will be pulled inside your working directory; you should cd into `stacks-usecase/pix2pix/openfaas/` before running the next commands so that `faas-cli` is able to find all needed files.

```bash
$ faas-cli template pull https://github.com/intel/stacks-templates-openfaas.git
```

#### Insert your pre-trained model into the Docker image

The Pix2Pix function uses a pre-trained model for inference, you should copy your desired pre-trained model inside `src`.

```bash
$ cp <model.h5> stacks-usecase/pix2pix/openfaas/src/generator_model.h5
```

### Build, push, deploy

In this step you will build a Docker image that will be consumed when deploying the Pix2Pix function in the OpenFaaS instance.
The Pix2Pix deployment uses a docker image pull request, thus the image that will be built should be available either on a public registry or on a private one. If you are using a private one, please refer to the OpenFaaS [documentation](https://docs.openfaas.com/deployment/kubernetes/#use-a-private-registry-with-kubernetes) for more information.

```bash
# Edit stack.yml so that the image points to your desired repository
image: <repository>/pix2pix-faas:0.1

$ faas-cli up -f ./stack.yml --gateway http://<localhost>:31112
```

`faas-cli up` will build the image for the function, push it to the specified container registry and deploy the function to the running OpenFaaS instance.

Once the above command has finished, you should be able to invoke your Pix2Pix function.

## Invoke Pix2Pix

You have two options for invoking your function:

#### Making POST requests on your host machine via CLI

The following command will return a base64 bytes object that you can later convert into an image object.

```bash
$ curl -X POST --data-binary @<path to input image> http://<localhost>:31112
```

#### Interacting via web UI

Follow instructions [here](https://github.com/intel/stacks-usecase/tree/master/pix2pix/pix2pix_website)
