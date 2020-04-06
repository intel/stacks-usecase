# Cassandra healthcare use case

This repository contains all the files required to deploy cassandra for the healthcare use case.

| **Directory** | **Description** |
|--------------------------|-----------------------| 
| **cassandra-upstream-chart**  |Helm chart for deploying a cassandra cluster on K8s, this requires [Helm](https://helm.sh/)|
| **deploy-local-storage-chart** |Helm chart for creating K8s local persistent volumes, it should be used before cassandra-upstream-chart, requires [Helm](https://helm.sh/)|
| **cql**                       |CQL file for creating the healthcare use case database and documentation on how to connect to it using `cqlsh` and `nodetool`|
| **cassandra-stress**          |Configuration files to run `cassandra-stress` against the healthcare use case database|
| **python**                    |Python examples on how to insert and retrieve blobs from the database using SSL and authentication, those scripts require the [Python driver for Cassandra](https://github.com/datastax/python-driver)|
