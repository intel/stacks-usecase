# Cassandra Helm Chart

## How to use
- Modify `values.yaml` according to your deployment
- If you want to provide custom configuration you should modify `files/conf/cassandra.yaml`. Remember to match seed addresses to the name of your helm deployment otherwise the nodes should not be able to reach eachother in the cluster.
- If you enabled encryption on `values.yaml`, create encryption certs using `files/conf/create-encryption-certs.sh`
- Run: 
```bash
helm install --name <deployment-name> --namespace <namespace-name> <path-to-this-directory>
```
