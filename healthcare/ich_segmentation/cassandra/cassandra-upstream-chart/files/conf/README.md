# Configuration files
When using `provideCustomConfig: true` in values.yaml, the files included in this directory are mounted as config files inside the pod, so 
more complex configurations can be provided in this way.

| **File** | **Description** |
| :--- | :-- |
| cassandra.yaml | File to configure cassandra, this file is used to provide specific options to cassandra running on the container, this example file includes configuration for authentication and encryption |
| cassandra-env.sh | File to configure cassandra environment variables, it overwrites default cassandra-env.sh, this example file enables authentication,SSL for JMX  and sets consistent rangemovement to false since K8s does not support static IPs |
| create-encryption-certs.sh | This bash script is used to create the files required for encryption, it must be run and then cassandra.yaml should be modified to use the generated files keystore and truststore in server-side and cassandra.cer for the clients connecting to casandra, the generated files should be placed in this directory so the helm chart can mount them into the cassandra containers |


