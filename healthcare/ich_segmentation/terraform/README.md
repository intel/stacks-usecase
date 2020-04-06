# Healthcare usecase infrastructure


The infrastructure for the Intracraneal Hemorrhage Detection usecase was deployed into [Google Cloud Platform](https://cloud.google.com/docs/overview), using Terraform as Infrastructure as Code ([IaC](https://en.wikipedia.org/wiki/Infrastructure_as_code)) tool.  

This allowed us to create, manage and provision the computing resources through definition files in a standardize way, in order to run the data analysis and to train a neural network, aiming to help radiologist to examine scans, speeding up the diagnosis process.

These scripts are located inside the terraform directory on this repository [https://github.com/intel/stacks-usecase](https://github.com/intel/stacks-usecase)/ich_segmentation.  

Its names are self explanatory, but here is a brief description of each of them.


**connections.tf** - Provider configuration, credentials, project and region definition.

**networks.tf** - Network definitions.

**kf-hc-cluster.tf** - Cluster and node pool specifications to run Kubeflow pipelines.

**dars-nodepoo.tf** - Data Analytics Reference Stack node pool definition, used to deploy Spark on Yarn cluster.

**cassandra-prod-pool.tf** - Node pool used to create a Cassandra DB cluster using persistent volumes. 

**variables.tf** - Configure variables used across the scripts.  


## Pre-requisites


You have access to a GCP project and are able to create a service account with the following roles: 

* Cloud Trace Admin
* Compute Admin
* Compute Storage Admin
* Kubernetes Engine Admin
* Kubernetes Engine Cluster Admin
* Service Account User
* Service Management Administrator
* Storage Object Admin 


[Creating and managing service accounts](https://cloud.google.com/iam/docs/creating-managing-service-accounts).   

Create and download its keys, these will have to be defined inside **variables.tf** file.  

Install **Terraform v0.12** on your machine [https://learn.hashicorp.com/terraform/getting-started/install.html](https://learn.hashicorp.com/terraform/getting-started/install.html)

Additionally, even that is not strictly necessary you can install Google Cloud SDK on your computer, this will allow you to connect with GCP directly from your terminal instead of using the Cloud Shell terminal or the Google Cloud web console to interact and query your resources [https://cloud.google.com/sdk/docs/quickstart-linux](https://cloud.google.com/sdk/docs/quickstart-linux)

Finally edit **variables.tf** file values accordingly.


## Deploy the infrastructure.


Placed into the terraform directory, initialize it, running: 

```bash
terraform init  
```

This command performs several different steps in order to prepare a working directory with Terraform configuration files for use.

Retrieve a preview of what will be executed and the resources that will be created based on the files in the current directory executing:

```bash
terraform plan  
```

If everything looks OK, then run:

```bash
terraform apply  
```

You will see again the list of resources to be created but this time you will be asked *Do you want to perform these actions?* Type *yes* and hit Enter to start the deployment, it will take a few minutes to complete.

A *terraform.tfstate* file will be created, containing the configuration for all the elements that were launched.

At the end you will have a cluster with three node pools ready to be configured.  Follow the instructions for each of them to complete the setup.


## Destroy the infrastructure


If you want to remove all the resources created, type:

```bash
terraform plan -destroy
```

This will get you a preview of the resouces to be deleted.

To destroy them permanently execute:

```bash
terraform destroy
```


